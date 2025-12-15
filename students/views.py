from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Count, Sum
from django.http import HttpResponse
from io import BytesIO
import qrcode
from .models import Student
from .forms import StudentRegistrationForm
from .email_service import send_student_registration_email, send_partner_notification_email, send_admin_notification_email
from partnerships.models import Partner, PartnershipCode


class StudentRegistrationView(CreateView):
    """Vue pour l'inscription des élèves"""
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('registration-success')

    def get_initial(self):
        initial = super().get_initial()
        # Pré-remplir le code si fourni en paramètre
        code = self.request.GET.get('code')
        if code:
            initial['referral_code'] = code.upper()
        return initial

    def get_context_data(self, **kwargs):
        from .models import Program
        context = super().get_context_data(**kwargs)
        code = self.request.GET.get('code')
        if code:
            context['code_from_qr'] = code.upper()
        context['programs'] = Program.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        student = self.object

        # Afficher email de confirmation dans le terminal
        self._print_confirmation_email(student)

        # Envoyer les 3 emails
        send_student_registration_email(student)
        send_partner_notification_email(student)
        send_admin_notification_email(student)

        messages.success(self.request, "Inscription reussie ! Merci d'avoir choisi notre ecole.")
        return response

    def _print_confirmation_email(self, student):
        """Affiche l'email de confirmation dans le terminal"""
        print("\n" + "="*80)
        print("📧 EMAIL DE CONFIRMATION D'INSCRIPTION")
        print("="*80)
        print(f"\nTo: {student.email}")
        print(f"From: noreply@ecole.com")
        print(f"Subject: Confirmation d'inscription - Bienvenue!")
        print("\n" + "-"*80)
        print(f"""
Bonjour {student.full_name},

Merci pour votre inscription! 🎉

📋 DÉTAILS DE VOTRE INSCRIPTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nom complet:        {student.full_name}
Email:              {student.email}
Téléphone:          {student.phone}
Programme:          {student.program.name}
Date d'inscription: {student.enrollment_date.strftime('%d/%m/%Y à %H:%M')}

🏪 PARTENAIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Partenaire: {student.partner.name if student.partner else 'N/A'}
Code utilisé: {student.referral_code}

Ce partenaire reçoit une commission pour chaque inscription réussie.

📝 PROCHAINES ÉTAPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Vérifiez tous les détails ci-dessus
2. Préparez vos documents si nécessaire
3. Consultez notre portail étudiant
4. Contactez-nous si vous avez des questions

Besoin d'aide?
Email: support@ecole.com
Téléphone: +213 XXX XXX XXX

Cordialement,
L'équipe de l'école
""")
        print("-"*80)
        print("="*80 + "\n")

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class RegistrationSuccessView(DetailView):
    """Vue de confirmation d'inscription"""
    model = Student
    template_name = 'students/registration-success.html'
    context_object_name = 'student'

    def get_object(self):
        # Récupère le dernier élève inscrit
        return Student.objects.order_by('-enrollment_date').first()


class PartnerDashboardView(DetailView):
    """Dashboard public pour les partenaires"""
    model = Partner
    template_name = 'students/partner-dashboard.html'
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


def generate_qr_code(request, code):
    """Génère un QR code pour un code de partenariat"""
    code = code.upper()

    # Vérifier que le code existe
    partnership_code = get_object_or_404(PartnershipCode, code=code, is_active=True)

    # Créer l'URL complète pour le QR code
    # URL: http://localhost:8000/register/?code=LIB4F6
    # Le code sera pré-rempli dans le formulaire
    base_url = request.build_absolute_uri('/register/')
    url_with_code = f"{base_url}?code={code}"

    # Générer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_with_code)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Retourner l'image
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


class QRCodeListView(TemplateView):
    """Affiche les QR codes pour chaque partenaire"""
    template_name = 'students/qr-codes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer tous les codes actifs
        codes = PartnershipCode.objects.filter(is_active=True).select_related('partner')

        codes_with_urls = []
        for code in codes:
            register_url = self.request.build_absolute_uri(f'/register/?code={code.code}')
            # Générer le QR code en base64 pour l'afficher directement
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(register_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            # Convertir en base64
            import base64
            from io import BytesIO
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

            codes_with_urls.append({
                'code': code.code,
                'partner': code.partner,
                'register_url': register_url,
                'qr_base64': f'data:image/png;base64,{img_base64}',
                'qr_file': f'{code.code.lower()}.png',
            })

        context['codes'] = codes_with_urls
        return context
