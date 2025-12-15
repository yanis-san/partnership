from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, F, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden, HttpResponse, FileResponse
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .models import Partner, Payment, PartnershipCode, PaymentReceipt, PartnershipRequest, PaymentCheckpoint
from .forms import PartnerCreationForm, QuickPaymentForm, PartnershipRequestForm
from students.models import Student
from datetime import datetime, timedelta
import qrcode
import io
import base64


class AdminLoginView(TemplateView):
    """Page de connexion admin sécurisée"""
    template_name = 'partnerships/admin-login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('admin-home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, "Connexion réussie!")
            return redirect('admin-home')
        else:
            messages.error(request, "Identifiants invalides ou accès refusé.")
            context = self.get_context_data()
            return self.render_to_response(context)


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal pour l'administration"""
    template_name = 'partnerships/admin-dashboard.html'
    login_url = 'admin-login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistiques globales
        total_partners = Partner.objects.filter(status='active').count()
        total_students_pending = Student.objects.filter(status='active', is_confirmed=False).count()
        total_students_confirmed = Student.objects.filter(status='active', is_confirmed=True).count()
        total_paid = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculer les montants via les propriétés des partenaires
        partners = Partner.objects.filter(status='active')
        total_earned = sum(p.total_earned for p in partners)  # Basé sur confirmés
        total_earned_real = sum(p.total_earned_real for p in partners)  # Basé sur confirmés
        remaining_balance = sum(p.remaining_balance for p in partners)  # Basé sur confirmés

        context['total_partners'] = total_partners
        context['total_students_pending'] = total_students_pending
        context['total_students_confirmed'] = total_students_confirmed
        context['total_earned'] = total_earned
        context['total_earned_real'] = total_earned_real
        context['total_paid'] = total_paid
        context['remaining_balance'] = remaining_balance

        # Partenaires avec leurs statistiques (réutiliser les objets déjà chargés)
        partners_for_display = sorted(partners, key=lambda x: x.total_students_confirmed, reverse=True)
        context['partners'] = partners_for_display

        # Paiements récents
        context['recent_payments'] = Payment.objects.select_related('partner').order_by('-created_at')[:10]

        # Statuts de paiement
        payment_stats = {
            'pending': Payment.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0,
            'completed': Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0,
            'cancelled': Payment.objects.filter(status='cancelled').aggregate(total=Sum('amount'))['total'] or 0,
        }
        context['payment_stats'] = payment_stats

        # Élèves récents
        context['recent_students'] = Student.objects.select_related('partner').order_by('-enrollment_date')[:10]

        return context


class AdminStatsView(UserPassesTestMixin, TemplateView):
    """Dashboard minimaliste pour les stats par partenaire - Superuser only"""
    template_name = 'partnerships/admin-stats.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer tous les partenaires avec stats
        partners_data = []
        for partner in Partner.objects.filter(status='active'):
            # Codes du partenaire
            codes = PartnershipCode.objects.filter(partner=partner, is_active=True)

            # Stats par code
            codes_stats = []
            for code in codes:
                pending_count = Student.objects.filter(referral_code=code.code, status='active', is_confirmed=False).count()
                confirmed_count = Student.objects.filter(referral_code=code.code, status='active', is_confirmed=True).count()
                earned = partner.commission_per_student * confirmed_count

                codes_stats.append({
                    'code': code.code,
                    'pending': pending_count,
                    'confirmed': confirmed_count,
                    'earned': earned,
                })

            total_pending = sum(c['pending'] for c in codes_stats)
            total_confirmed = sum(c['confirmed'] for c in codes_stats)
            total_earned = sum(c['earned'] for c in codes_stats)

            partners_data.append({
                'partner': partner,
                'type': partner.get_partner_type_display(),
                'codes': codes_stats,
                'total_pending': total_pending,
                'total_confirmed': total_confirmed,
                'total_earned': total_earned,
            })

        context['partners_data'] = partners_data
        context['total_partners'] = len(partners_data)
        context['total_pending'] = sum(p['total_pending'] for p in partners_data)
        context['total_confirmed'] = sum(p['total_confirmed'] for p in partners_data)
        context['total_earned'] = sum(p['total_earned'] for p in partners_data)

        return context


class PartnerDashboardPublicView(DetailView):
    """Dashboard public pour les partenaires"""
    model = Partner
    template_name = 'partnerships/partner-dashboard-public.html'
    context_object_name = 'partner'

    def get_object(self):
        # Récupère le partenaire via son code partenaire
        code = self.kwargs.get('code')
        partnership_code = get_object_or_404(PartnershipCode, code=code.upper())
        return partnership_code.partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner = self.get_object()

        context['students'] = partner.students.filter(status='active').order_by('-enrollment_date')
        context['total_students'] = partner.total_students
        context['total_earned'] = partner.total_earned
        context['total_paid'] = partner.total_paid
        context['remaining_balance'] = partner.remaining_balance
        context['payment_status'] = partner.payment_status
        context['partnership_codes'] = partner.partnership_codes.filter(is_active=True)

        return context


class PaymentsDashboardView(UserPassesTestMixin, TemplateView):
    """Dashboard des paiements - Superuser only"""
    template_name = 'partnerships/payments-dashboard.html'

    def test_func(self):
        """Vérifier que l'utilisateur est superuser"""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Rediriger si non autorisé"""
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Accès refusé. Vous devez être superuser.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer tous les partenaires actifs
        partners = Partner.objects.filter(status='active')

        # Calculer les montants pour chaque partenaire
        payment_data = []
        for p in partners:
            # Calculer directement depuis les propriétés
            total_earned = p.total_earned
            total_paid = p.total_paid
            remaining = max(total_earned - total_paid, 0)

            payment_data.append({
                'partner': p,
                'total_earned': total_earned or 0,
                'total_paid': total_paid or 0,
                'remaining': remaining or 0,
                'status': p.payment_status,
                'student_count': p.total_students or 0
            })

        # Trier par montant restant décroissant
        payment_data.sort(key=lambda x: x['remaining'], reverse=True)

        # Totaux
        context['payment_data'] = payment_data
        context['total_partners'] = len(payment_data)
        context['grand_total_earned'] = sum(p['total_earned'] for p in payment_data)
        context['grand_total_paid'] = sum(p['total_paid'] for p in payment_data)
        context['grand_total_remaining'] = sum(p['remaining'] for p in payment_data)

        return context


class PartnerLoginView(TemplateView):
    """Page de login pour les partenaires avec protection contre les tentatives brutes"""
    template_name = 'partnerships/partner-login.html'
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 15  # minutes

    def _get_login_attempts(self):
        """Récupère le nombre de tentatives de login depuis la session"""
        return {
            'count': self.request.session.get('login_attempts', 0),
            'last_attempt': self.request.session.get('last_login_attempt', None),
        }

    def _check_locked_out(self):
        """Vérifie si l'utilisateur est bloqué"""
        attempts = self._get_login_attempts()
        if attempts['count'] >= self.MAX_LOGIN_ATTEMPTS and attempts['last_attempt']:
            last_attempt = datetime.fromisoformat(attempts['last_attempt'])
            lockout_time = last_attempt + timedelta(minutes=self.LOCKOUT_DURATION)
            if datetime.now() < lockout_time:
                remaining = int((lockout_time - datetime.now()).total_seconds() / 60)
                return True, f"Trop de tentatives. Réessayez dans {remaining} minute(s)."
        return False, None

    def _increment_attempts(self):
        """Augmente le compteur de tentatives"""
        attempts = self.request.session.get('login_attempts', 0)
        self.request.session['login_attempts'] = attempts + 1
        self.request.session['last_login_attempt'] = datetime.now().isoformat()

    def _reset_attempts(self):
        """Réinitialise le compteur après login réussi"""
        self.request.session['login_attempts'] = 0
        self.request.session['last_login_attempt'] = None

    def get(self, request):
        """Affiche la page de login"""
        locked_out, error = self._check_locked_out()
        context = {}
        if locked_out:
            context['error'] = error
        return render(request, self.template_name, context)

    def post(self, request):
        """Traite le formulaire de login"""
        email = request.POST.get('email', '').strip()
        code = request.POST.get('code', '').strip().upper()
        password = request.POST.get('password', '')

        # Vérifier le verrouillage
        locked_out, error = self._check_locked_out()
        if locked_out:
            return render(request, self.template_name, {'error': error})

        # Valider les champs
        if not all([email, code, password]):
            error = "Tous les champs sont requis"
            self._increment_attempts()
            return render(request, self.template_name, {'error': error})

        # Vérifier les identifiants
        try:
            partnership_code = PartnershipCode.objects.get(code=code, is_active=True)
            partner = partnership_code.partner

            # Vérifier email et mot de passe
            if partner.email != email:
                self._increment_attempts()
                error = "Email, code ou mot de passe incorrect"
                return render(request, self.template_name, {'error': error})

            if not partner.check_password(password):
                self._increment_attempts()
                error = "Email, code ou mot de passe incorrect"
                return render(request, self.template_name, {'error': error})

            # Login réussi
            self._reset_attempts()
            request.session['partner_id'] = str(partner.id)
            request.session['partner_name'] = partner.name
            request.session['partner_code'] = code
            request.session.set_expiry(timedelta(hours=24))  # Session de 24h

            messages.success(request, f"Bienvenue {partner.name}!")
            return redirect('partner-dashboard-personal')

        except PartnershipCode.DoesNotExist:
            self._increment_attempts()
            error = "Email, code ou mot de passe incorrect"
            return render(request, self.template_name, {'error': error})


class PartnerDashboardPersonalView(TemplateView):
    """Dashboard personnel pour chaque partenaire"""
    template_name = 'partnerships/partner-dashboard-personal.html'

    def get(self, request):
        partner_id = request.session.get('partner_id')

        if not partner_id:
            return redirect('partner-login')

        partner = get_object_or_404(Partner, id=partner_id)

        # ====== DEPUIS LE DÉBUT ======
        total_all_time_confirmed = partner.students.filter(
            status='active', is_confirmed=True
        ).count()
        total_revenue_all_time = partner.commission_per_student * total_all_time_confirmed
        total_paid_all_checkpoints = partner.payment_checkpoints.aggregate(
            total=Sum('amount_paid')
        )['total'] or 0
        total_remaining_payment = total_revenue_all_time - total_paid_all_checkpoints

        # ====== DEPUIS DERNIER CHECKPOINT ======
        students_since_checkpoint = partner.total_students_confirmed
        revenue_since_checkpoint = partner.commission_per_student * students_since_checkpoint

        # ====== EN ATTENTE ======
        pending_students = partner.students.filter(
            status='active', is_confirmed=False
        ).count()

        context = {
            'partner': partner,
            # Depuis checkpoint
            'pending_count': pending_students,
            'students_since_checkpoint': students_since_checkpoint,
            'revenue_since_checkpoint': revenue_since_checkpoint,
            # Total depuis le début
            'total_all_time_confirmed': total_all_time_confirmed,
            'total_revenue_all_time': total_revenue_all_time,
            'total_paid_all_checkpoints': total_paid_all_checkpoints,
            'total_remaining_payment': total_remaining_payment,
            # Autres données
            'students': partner.students.filter(status='active').order_by('-enrollment_date'),
            'checkpoints': partner.payment_checkpoints.all(),
            'partnership_codes': partner.partnership_codes.filter(is_active=True)
        }

        return render(request, self.template_name, context)


def partner_logout_view(request):
    """Déconnexion du partenaire"""
    if 'partner_id' in request.session:
        del request.session['partner_id']
    if 'partner_name' in request.session:
        del request.session['partner_name']
    if 'partner_code' in request.session:
        del request.session['partner_code']

    return redirect('student-register')


def admin_logout_view(request):
    """Déconnexion de l'admin"""
    logout(request)
    messages.success(request, "Déconnexion réussie.")
    return redirect('student-register')


class PartnerPaymentHistoryView(TemplateView):
    """Affiche l'historique des paiements pour un partenaire connecté"""
    template_name = 'partnerships/partner-payment-history.html'

    def get(self, request):
        partner_id = request.session.get('partner_id')

        if not partner_id:
            return redirect('partner-login')

        partner = get_object_or_404(Partner, id=partner_id)

        # Récupérer les reçus (les plus récents d'abord)
        receipts = PaymentReceipt.objects.filter(
            payment__partner=partner
        ).select_related('payment').order_by('-created_at')

        # Récupérer les montants du partenaire
        partner_paid_amount = partner.total_paid
        partner_confirmed_count = partner.total_students_confirmed
        partner_confirmed_amount = partner.commission_per_student * partner_confirmed_count
        partner_solde = partner_confirmed_amount - partner_paid_amount

        context = {
            'partner': partner,
            'receipts': receipts,
            'last_receipt': receipts.first() if receipts.exists() else None,
            'partner_paid_amount': partner_paid_amount,
            'partner_confirmed_amount': partner_confirmed_amount,
            'partner_solde': partner_solde,
        }

        return render(request, self.template_name, context)


class AdminPartnerCreationView(UserPassesTestMixin, TemplateView):
    """Vue pour créer rapidement un partenaire et générer un QR code"""
    template_name = 'partnerships/admin-create-partner.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PartnerCreationForm()
        return context

    def post(self, request):
        form = PartnerCreationForm(request.POST)

        if form.is_valid():
            partner = form.save()

            # Créer un code de partenariat
            partnership_code = PartnershipCode.objects.create(
                partner=partner,
                code=partner.partner_code,
                is_active=True
            )

            # Générer le QR code (qui pointe vers l'URL d'inscription avec le code)
            qr_data = self._generate_qr_code(partnership_code.code, request)

            context = {
                'form': PartnerCreationForm(),
                'partner': partner,
                'code': partnership_code.code,
                'qr_data': qr_data,
                'success': True,
                'login_url': request.build_absolute_uri('/partnerships/login/'),
            }

            return render(request, self.template_name, context)

        return render(request, self.template_name, {'form': form, 'success': False})

    def _generate_qr_code(self, code, request):
        """Génère un QR code en base64 pointant vers le formulaire d'inscription avec le code"""
        # Construire l'URL d'inscription avec le code comme paramètre
        registration_url = request.build_absolute_uri(f'/register/?code={code}')

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(registration_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convertir l'image en base64 pour l'afficher dans le template
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return img_str


class AdminStudentConfirmationView(UserPassesTestMixin, TemplateView):
    """Dashboard pour confirmer les inscriptions étudiants et voir les montants"""
    template_name = 'partnerships/admin-student-confirmation.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer tous les partenaires actifs avec leurs étudiants
        partners = Partner.objects.filter(status='active').prefetch_related('students')

        partners_data = []
        for partner in partners:
            # Étudiants en attente de confirmation
            pending_students = partner.students.filter(status='active', is_confirmed=False)
            # Étudiants confirmés
            confirmed_students = partner.students.filter(status='active', is_confirmed=True)

            pending_count = pending_students.count()
            confirmed_count = confirmed_students.count()
            pending_amount = partner.commission_per_student * pending_count
            confirmed_amount = partner.commission_per_student * confirmed_count
            paid_amount = partner.total_paid
            solde = confirmed_amount - paid_amount

            partners_data.append({
                'partner': partner,
                'pending_students': pending_students,
                'confirmed_students': confirmed_students,
                'pending_count': pending_count,
                'confirmed_count': confirmed_count,
                'pending_amount': pending_amount,
                'confirmed_amount': confirmed_amount,
                'paid_amount': paid_amount,
                'solde': solde,
                'total_students': pending_count + confirmed_count,
            })

        context['partners_data'] = partners_data
        context['total_pending'] = sum(p['pending_amount'] for p in partners_data)
        context['total_confirmed'] = sum(p['confirmed_amount'] for p in partners_data)

        return context


class ConfirmStudentHTMXView(UserPassesTestMixin, View):
    """Endpoint HTMX pour confirmer un étudiant"""

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, student_id):
        """Confirme l'inscription d'un étudiant"""
        student = get_object_or_404(Student, id=student_id)
        partner = student.partner
        student.is_confirmed = True
        student.save()

        # Calculer les montants
        partner_pending_count = partner.students.filter(status='active', is_confirmed=False).count()
        partner_confirmed_count = partner.students.filter(status='active', is_confirmed=True).count()
        partner_pending_amount = partner.commission_per_student * partner_pending_count
        partner_confirmed_amount = partner.commission_per_student * partner_confirmed_count
        partner_paid_amount = partner.total_paid
        partner_solde = partner_confirmed_amount - partner_paid_amount

        # Retourner la ligne mise à jour ET les totaux du partenaire
        return render(request, 'partnerships/partials/student-row-with-totals.html', {
            'student': student,
            'partner': partner,
            'partner_pending_count': partner_pending_count,
            'partner_confirmed_count': partner_confirmed_count,
            'partner_pending_amount': partner_pending_amount,
            'partner_confirmed_amount': partner_confirmed_amount,
            'partner_paid_amount': partner_paid_amount,
            'partner_solde': partner_solde,
        })


class PaymentReceiptFormView(UserPassesTestMixin, View):
    """Affiche le formulaire HTMX pour ajouter un reçu de paiement"""

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, partner_id):
        """Affiche le formulaire d'upload du reçu"""
        partner = get_object_or_404(Partner, id=partner_id)
        form = QuickPaymentForm()

        return render(request, 'partnerships/partials/payment-receipt-form.html', {
            'form': form,
            'partner': partner,
        })


class PaymentReceiptUploadView(UserPassesTestMixin, View):
    """Traite l'upload du reçu et met à jour les paiements"""

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, partner_id):
        """Traite l'upload et crée/met à jour le paiement"""
        partner = get_object_or_404(Partner, id=partner_id)
        form = QuickPaymentForm(request.POST, request.FILES)

        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            receipt_image = form.cleaned_data['receipt_image']
            notes = form.cleaned_data.get('notes', '')

            # Créer un paiement
            payment = Payment.objects.create(
                partner=partner,
                amount=amount_paid,
                status=Payment.COMPLETED,
                completed_at=timezone.now(),
                notes=notes
            )
            payment.remaining_amount = 0
            payment.save()

            # Créer le reçu associé
            receipt = PaymentReceipt.objects.create(
                payment=payment,
                receipt_image=receipt_image,
                amount_paid=amount_paid,
                notes=notes
            )

            # Rediriger vers la page d'historique
            return redirect('payment-history', partner_id=partner.id)
        else:
            return render(request, 'partnerships/partials/payment-receipt-form.html', {
                'form': form,
                'partner': partner,
                'errors': form.errors
            }, status=400)


class PaymentReceiptListView(UserPassesTestMixin, TemplateView):
    """Affiche la liste des reçus de paiement pour un partenaire"""
    template_name = 'partnerships/partner-payment-history.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, partner_id, **kwargs):
        context = super().get_context_data(**kwargs)
        partner = get_object_or_404(Partner, id=partner_id)

        # Récupérer les reçus (les plus récents d'abord)
        receipts = PaymentReceipt.objects.filter(
            payment__partner=partner
        ).select_related('payment').order_by('-created_at')

        # Récupérer les montants du partenaire
        partner_paid_amount = partner.total_paid
        partner_confirmed_count = partner.students.filter(status='active', is_confirmed=True).count()
        partner_confirmed_amount = partner.commission_per_student * partner_confirmed_count
        partner_solde = partner_confirmed_amount - partner_paid_amount

        context['partner'] = partner
        context['receipts'] = receipts
        context['last_receipt'] = receipts.first() if receipts.exists() else None
        context['partner_paid_amount'] = partner_paid_amount
        context['partner_confirmed_amount'] = partner_confirmed_amount
        context['partner_solde'] = partner_solde

        return context


class AdminHomeView(UserPassesTestMixin, TemplateView):
    """Page d'accueil du centre de contrôle admin"""
    template_name = 'partnerships/admin-home.html'
    login_url = 'admin-login'

    def test_func(self):
        return self.request.user.is_superuser


class PartnershipRequestView(CreateView):
    """Vue pour soumettre une demande de partenariat"""
    model = PartnershipRequest
    form_class = PartnershipRequestForm
    template_name = 'partnerships/partnership-request.html'
    success_url = reverse_lazy('partnership-request-success')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Envoyer un email au backend avec les informations du partenaire
        request_obj = form.instance
        self._send_partnership_email(request_obj)

        return response

    def _send_partnership_email(self, request_obj):
        """Envoie un email avec les détails de la demande de partenariat"""
        subject = f"Nouvelle demande de partenariat - {request_obj.business_name}"

        message = f"""
Nouvelle demande de partenariat reçue:

INFORMATIONS DU COMMERCE
========================
Nom: {request_obj.business_name}
Type: {request_obj.get_business_type_display()}
Email: {request_obj.email}
Téléphone: {request_obj.phone}
Adresse: {request_obj.address}

MESSAGE
=======
{request_obj.message}

---
Date de soumission: {request_obj.created_at.strftime('%d/%m/%Y à %H:%M')}
ID de demande: {request_obj.id}
        """

        try:
            send_mail(
                subject,
                message,
                'noreply@affiliation-irl.fr',
                ['contact@affiliation-irl.fr'],  # À adapter avec votre email
                fail_silently=False,
            )
        except Exception as e:
            # Log l'erreur mais ne bloque pas la soumission du formulaire
            print(f"Erreur lors de l'envoi du mail: {e}")


class PartnershipRequestSuccessView(TemplateView):
    """Page de confirmation après soumission de demande de partenariat"""
    template_name = 'partnerships/partnership-request-success.html'


class AdminPartnersManagementView(UserPassesTestMixin, TemplateView):
    """Vue pour gérer les partenaires et confirmer les étudiants"""
    template_name = 'partnerships/admin-partners-management.html'
    login_url = '/admin/'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer tous les partenaires avec leurs infos
        partners = Partner.objects.filter(status='active').prefetch_related(
            'students', 'payment_checkpoints'
        ).order_by('-created_at')

        # Ajouter les stats pour chaque partenaire
        partners_data = []
        for partner in partners:
            pending_students = partner.students.filter(
                status='active', is_confirmed=False
            ).order_by('-enrollment_date')

            # ====== DEPUIS LE DÉBUT ======
            total_confirmed_all_time = partner.students.filter(
                status='active', is_confirmed=True
            ).count()
            total_revenue_all_time = partner.commission_per_student * total_confirmed_all_time
            total_paid_all_checkpoints = partner.payment_checkpoints.aggregate(
                total=Sum('amount_paid')
            )['total'] or 0
            total_remaining_payment = total_revenue_all_time - total_paid_all_checkpoints

            # ====== DEPUIS DERNIER CHECKPOINT ======
            students_since_checkpoint = partner.total_students_confirmed
            revenue_since_checkpoint = partner.commission_per_student * students_since_checkpoint

            partners_data.append({
                'partner': partner,
                'pending_students': pending_students,
                'pending_count': pending_students.count(),
                # Depuis checkpoint
                'confirmed_count': students_since_checkpoint,
                'revenue_since_checkpoint': revenue_since_checkpoint,
                # Total depuis le début
                'total_confirmed_all_time': total_confirmed_all_time,
                'total_revenue_all_time': total_revenue_all_time,
                'total_paid_all_checkpoints': total_paid_all_checkpoints,
                'remaining_payment': total_remaining_payment,
                'last_checkpoint': partner.get_last_checkpoint,
            })

        context['partners_data'] = partners_data
        return context


class AdminCheckpointCreateView(UserPassesTestMixin, View):
    """Vue pour créer rapidement un checkpoint"""
    login_url = '/admin/'

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, partner_id):
        """Créer un checkpoint"""
        from django.http import JsonResponse
        import traceback

        try:
            partner = get_object_or_404(Partner, id=partner_id)
            amount_paid = request.POST.get('amount_paid')
            notes = request.POST.get('notes', '')

            if not amount_paid:
                return JsonResponse({'error': 'Montant requis'}, status=400)

            try:
                amount_paid = float(amount_paid)
                checkpoint = PaymentCheckpoint.objects.create(
                    partner=partner,
                    amount_paid=amount_paid,
                    notes=notes
                    # checkpoint_date sera auto-rempli à aujourd'hui
                )
                return JsonResponse({
                    'success': True,
                    'message': f'Checkpoint créé: {amount_paid} DA'
                })
            except ValueError:
                return JsonResponse({'error': 'Montant invalide'}, status=400)
        except Exception as e:
            print(f"Erreur checkpoint: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)


class AdminConfirmStudentView(UserPassesTestMixin, View):
    """Vue pour confirmer un étudiant"""
    login_url = '/admin/'

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, student_id):
        """Confirmer un étudiant"""
        from django.http import JsonResponse

        student = get_object_or_404(Student, id=student_id)
        student.is_confirmed = True
        student.save()

        return JsonResponse({
            'success': True,
            'message': f'{student.full_name} confirmé'
        })


class AdminPartnerDetailView(UserPassesTestMixin, TemplateView):
    """Vue pour afficher les détails d'un partenaire"""
    template_name = 'partnerships/admin-partner-detail.html'
    login_url = '/admin/'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner_id = kwargs.get('partner_id')

        partner = get_object_or_404(Partner, id=partner_id)

        # Récupérer tous les étudiants du partenaire
        all_students = partner.students.filter(status='active').order_by('-enrollment_date')
        pending_students = all_students.filter(is_confirmed=False)
        confirmed_students = all_students.filter(is_confirmed=True)

        # Récupérer l'historique des checkpoints
        checkpoints = partner.payment_checkpoints.all()

        # ====== BILAN TOTAL (depuis le début) ======
        # Calculer le total payé de tous les checkpoints
        total_paid_all_checkpoints = checkpoints.aggregate(total=Sum('amount_paid'))['total'] or 0

        # Tous les étudiants confirmés (depuis le début)
        total_all_time_confirmed = partner.students.filter(
            status='active', is_confirmed=True
        ).count()
        total_revenue_all_time = partner.commission_per_student * total_all_time_confirmed

        # Solde global = Revenu total - Total payé
        total_remaining_payment = total_revenue_all_time - total_paid_all_checkpoints

        # ====== REVENU DEPUIS DERNIER CHECKPOINT ======
        # Étudiants confirmés APRÈS le dernier checkpoint
        last_checkpoint = partner.get_last_checkpoint
        if last_checkpoint:
            revenue_since_checkpoint = partner.commission_per_student * partner.total_students_confirmed
            students_since_checkpoint = partner.total_students_confirmed
        else:
            # Pas de checkpoint, donc tout est "depuis dernier checkpoint"
            revenue_since_checkpoint = total_revenue_all_time
            students_since_checkpoint = total_all_time_confirmed

        context.update({
            'partner': partner,
            'all_students': all_students,
            'pending_students': pending_students,
            'confirmed_students': confirmed_students,
            'pending_count': pending_students.count(),
            'confirmed_count': confirmed_students.count(),
            'checkpoints': checkpoints,
            # Total depuis le début
            'total_paid_all_checkpoints': total_paid_all_checkpoints,
            'total_all_time_confirmed': total_all_time_confirmed,
            'total_revenue_all_time': total_revenue_all_time,
            'total_remaining_payment': total_remaining_payment,
            # Depuis dernier checkpoint
            'students_since_checkpoint': students_since_checkpoint,
            'revenue_since_checkpoint': revenue_since_checkpoint,
        })

        return context


class PartnerCodesView(TemplateView):
    """Affiche les codes et QR codes du partenaire"""
    template_name = 'partnerships/partner-codes.html'

    def get(self, request):
        partner_id = request.session.get('partner_id')

        if not partner_id:
            return redirect('partner-login')

        partner = get_object_or_404(Partner, id=partner_id)
        codes = partner.partnership_codes.filter(is_active=True)

        context = {
            'partner': partner,
            'codes': codes,
        }

        return render(request, self.template_name, context)


class AdminPartnerCodesView(UserPassesTestMixin, TemplateView):
    """Affiche les codes et QR codes d'un partenaire (admin)"""
    template_name = 'partnerships/admin-partner-codes.html'
    login_url = '/admin/'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, partner_id=None):
        if partner_id:
            partner = get_object_or_404(Partner, id=partner_id)
        else:
            partner_id = request.GET.get('partner_id')
            if not partner_id:
                return redirect('admin-home')
            partner = get_object_or_404(Partner, id=partner_id)

        codes = partner.partnership_codes.filter(is_active=True)

        context = {
            'partner': partner,
            'codes': codes,
        }

        return render(request, self.template_name, context)


class GenerateCodePDFView(View):
    """Génère un PDF avec le code et QR code"""

    def get(self, request, code_id):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from PIL import Image
        import tempfile
        import os

        # Vérifier si c'est un partenaire connecté ou un admin
        partner_id = request.session.get('partner_id')
        is_admin = request.user.is_superuser

        if not partner_id and not is_admin:
            return redirect('partner-login')

        code_obj = get_object_or_404(PartnershipCode, id=code_id)

        # Vérifier les permissions
        if partner_id and str(code_obj.partner.id) != partner_id:
            return HttpResponseForbidden("Vous n'avez pas accès à ce code")

        # Chemin du logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo_torii.png')

        # Construire l'URL d'inscription avec le code pré-rempli
        from django.urls import reverse
        registration_url = request.build_absolute_uri(reverse('student-register'))
        registration_url_with_code = f"{registration_url}?code={code_obj.code}"

        # Générer le QR code avec l'URL complète (pas juste le code)
        qr = qrcode.QRCode(version=2, box_size=10, border=2)
        qr.add_data(registration_url_with_code)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Sauvegarder le QR code temporairement
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_qr_file:
            qr_tmp_path = tmp_qr_file.name
            qr_img.save(qr_tmp_path, format='PNG')

        # Créer le PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4

        # Logo en haut à gauche (très gros)
        if os.path.exists(logo_path):
            logo_size_pdf = 5 * cm
            c.drawImage(logo_path, 0.5*cm, height - 5.5*cm, width=logo_size_pdf, height=logo_size_pdf)

        # Titre
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height - 6*cm, "CODE PARTENAIRE")

        # Sous-titre avec Institut Torii
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height - 7*cm, "Institut Torii")

        # Code (gros)
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(width/2, height - 10.5*cm, code_obj.code)

        # QR Code avec logo
        try:
            qr_size = 7*cm
            qr_x = (width - qr_size) / 2
            qr_y = height - 14*cm
            c.drawImage(qr_tmp_path, qr_x, qr_y, width=qr_size, height=qr_size)
        finally:
            os.unlink(qr_tmp_path)

        # Description
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, qr_y - 1*cm, f"Partenaire: {code_obj.partner.name}")
        c.drawCentredString(width/2, qr_y - 1.5*cm, "Scannez le code QR pour vous inscrire")

        c.save()
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Code_{code_obj.code}.pdf"'
        return response
