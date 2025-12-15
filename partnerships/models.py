from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Partner(models.Model):
    """Modèle pour les partenaires (librairies, magasins, cafés, etc.)"""

    # Types de partenaires
    PARTNER_TYPES = [
        ('LIB', 'Librairie'),
        ('JV', 'Magasin Jeux Vidéo'),
        ('SUP', 'Superette'),
        ('CAF', 'Café'),
        ('BOO', 'Bouquinerie'),
        ('MAG', 'Magasin Général'),
        ('IND', 'Indépendant'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nom du partenaire")
    partner_type = models.CharField(
        max_length=3,
        choices=PARTNER_TYPES,
        default='LIB',
        verbose_name="Type de partenaire"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    contact_person = models.CharField(max_length=255, blank=True, verbose_name="Personne de contact")
    address = models.TextField(blank=True, verbose_name="Adresse")

    # Compte utilisateur associé
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='partner',
        verbose_name="Compte utilisateur"
    )

    # Commission par étudiant inscrit (en DA)
    commission_per_student = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000,
        verbose_name="Commission par élève (DA)"
    )

    # Statut du partenariat
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    STATUS_CHOICES = [
        (ACTIVE, 'Actif'),
        (INACTIVE, 'Inactif'),
        (SUSPENDED, 'Suspendu'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
        verbose_name="Statut"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.partner_code})"

    @property
    def partner_code(self):
        """Génère un code unique pour le partenaire basé sur son type et son ID"""
        # Format: TYPE_PREFIX + 3 caractères de l'UUID
        code_str = str(self.id)[:3].upper()
        return f"{self.partner_type}{code_str}"

    @property
    def get_last_checkpoint(self):
        """Récupère le dernier checkpoint (point de contrôle)"""
        return self.payment_checkpoints.first()

    @property
    def total_paid_at_checkpoint(self):
        """Montant total payé jusqu'au dernier checkpoint"""
        checkpoint = self.get_last_checkpoint
        if checkpoint:
            return checkpoint.amount_paid
        return 0

    @property
    def total_students(self):
        """Nombre total d'élèves en attente de confirmation"""
        return self.students.filter(is_confirmed=False).count()

    @property
    def total_students_confirmed(self):
        """Nombre d'élèves confirmés depuis le dernier checkpoint"""
        checkpoint = self.get_last_checkpoint
        if checkpoint:
            # Compte les étudiants confirmés APRÈS le checkpoint (basé sur updated_at)
            return self.students.filter(
                is_confirmed=True,
                updated_at__gt=checkpoint.checkpoint_date
            ).count()
        # Si pas de checkpoint, compte tous les confirmés
        return self.students.filter(is_confirmed=True).count()

    @property
    def total_students_confirmed_all_time(self):
        """Nombre TOTAL d'élèves confirmés (depuis le début)"""
        return self.students.filter(is_confirmed=True).count()

    @property
    def total_earned(self):
        """Montant total PROJETÉ depuis le dernier checkpoint"""
        return self.commission_per_student * self.total_students_confirmed

    @property
    def total_earned_real(self):
        """Montant total RÉEL depuis le dernier checkpoint"""
        return self.commission_per_student * self.total_students_confirmed

    @property
    def total_paid(self):
        """Montant total déjà payé (sum des checkpoints)"""
        return self.payment_checkpoints.aggregate(
            total=Sum('amount_paid')
        )['total'] or 0

    @property
    def revenue_estimated(self):
        """Revenu estimé depuis le dernier checkpoint"""
        return self.total_earned

    @property
    def revenue_real(self):
        """Revenu réel depuis le dernier checkpoint"""
        return self.total_earned_real

    @property
    def remaining_balance(self):
        """Montant restant à payer depuis le dernier checkpoint"""
        return self.revenue_real

    @property
    def payment_status(self):
        """Statut: En attente, Payé en partie, ou Payé"""
        if self.revenue_real == 0:
            return "Aucun gain"
        if self.remaining_balance == 0:
            return "Payé"
        return "En attente"

    def set_password(self, raw_password):
        """Définir le mot de passe hashé pour la librairie"""
        if self.user:
            self.user.set_password(raw_password)
            self.user.save()

    def check_password(self, raw_password):
        """Vérifier si le mot de passe est correct"""
        if self.user:
            return self.user.check_password(raw_password)
        return False


class PartnershipCode(models.Model):
    """Modèle pour tracker les codes de partenariat"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='partnership_codes',
        verbose_name="Partenaire"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code partenaire"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Code de partenariat"
        verbose_name_plural = "Codes de partenariat"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.partner.name}"

    @property
    def students_count(self):
        """Nombre d'étudiants inscrits avec ce code (en attente)"""
        from students.models import Student
        return Student.objects.filter(referral_code=self.code, status='active', is_confirmed=False).count()

    @property
    def confirmed_count(self):
        """Nombre d'étudiants confirmés avec ce code"""
        from students.models import Student
        return Student.objects.filter(referral_code=self.code, status='active', is_confirmed=True).count()

    @property
    def total_earned(self):
        """Montant généré par ce code (basé sur les confirmés)"""
        return self.partner.commission_per_student * self.confirmed_count


class Payment(models.Model):
    """Modèle pour gérer les paiements aux partenaires"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Partenaire"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant à payer (DA)"
    )

    # Montant restant à payer (calculé automatiquement)
    remaining_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant restant (DA)"
    )

    # Statut du paiement
    PENDING = 'pending'
    PARTIAL = 'partial'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Non payé'),
        (PARTIAL, 'Partiel'),
        (COMPLETED, 'Payé'),
        (CANCELLED, 'Annulé'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name="Statut"
    )

    # Références de paiement
    reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Référence de paiement"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de paiement")

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-created_at']

    def __str__(self):
        return f"Paiement {self.amount} DA - {self.partner.name} ({self.status})"

    def update_payment_status(self, paid_amount=None):
        """Mettre à jour automatiquement le statut et le montant restant"""
        if paid_amount is None:
            # Utiliser le montant payé depuis l'admin
            paid_amount = self.amount - self.remaining_amount

        # Calculer le montant restant
        self.remaining_amount = max(self.amount - paid_amount, 0)

        # Déterminer le statut automatiquement
        if self.remaining_amount == 0:
            self.status = self.COMPLETED
            self.completed_at = timezone.now()
        elif self.remaining_amount < self.amount:
            self.status = self.PARTIAL
            self.completed_at = None
        else:
            self.status = self.PENDING
            self.completed_at = None

    def save(self, *args, **kwargs):
        """Mettre à jour automatiquement les champs avant de sauvegarder"""
        self.update_payment_status()
        super().save(*args, **kwargs)

    def mark_as_completed(self):
        """Marquer le paiement comme complété"""
        self.status = self.COMPLETED
        self.remaining_amount = 0
        self.completed_at = timezone.now()
        self.save()

    def mark_as_pending(self):
        """Marquer le paiement comme en attente"""
        self.status = self.PENDING
        self.remaining_amount = self.amount
        self.completed_at = None
        self.save()


class PaymentReceipt(models.Model):
    """Modèle pour gérer les reçus de paiement (photos, documents)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name='receipt',
        verbose_name="Paiement associé"
    )

    # Image du reçu
    receipt_image = models.ImageField(
        upload_to='receipts/%Y/%m/%d/',
        verbose_name="Photo du reçu",
        help_text="Prenez une photo du reçu de paiement"
    )

    # Montant saisi lors de l'upload
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant payé (DA)"
    )

    # Notes optionnelles
    notes = models.TextField(
        blank=True,
        verbose_name="Notes (ex: mode de paiement, date du paiement)"
    )

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Reçu de paiement"
        verbose_name_plural = "Reçus de paiement"
        ordering = ['-created_at']

    def __str__(self):
        return f"Reçu {self.amount_paid} DA - {self.payment.partner.name} ({self.created_at.strftime('%d/%m/%Y')})"


class PaymentCheckpoint(models.Model):
    """Modèle pour tracker les points de contrôle des paiements"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='payment_checkpoints',
        verbose_name="Partenaire"
    )
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant payé (DA)"
    )
    checkpoint_date = models.DateTimeField(
        verbose_name="Date du paiement",
        blank=True,
        null=True,
        help_text="Laissez vide pour utiliser la date d'aujourd'hui"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes du paiement"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création du checkpoint")

    class Meta:
        verbose_name = "Point de contrôle paiement"
        verbose_name_plural = "Points de contrôle paiements"
        ordering = ['-checkpoint_date']

    def save(self, *args, **kwargs):
        """Remplir automatiquement checkpoint_date si vide"""
        if not self.checkpoint_date:
            self.checkpoint_date = timezone.now()
        # S'assurer que amount_paid est un Decimal
        from decimal import Decimal
        if isinstance(self.amount_paid, (int, float)):
            self.amount_paid = Decimal(str(self.amount_paid))
        super().save(*args, **kwargs)

    def __str__(self):
        date_str = self.checkpoint_date.strftime('%d/%m/%Y') if self.checkpoint_date else 'N/A'
        return f"{self.partner.name} - {self.amount_paid} DA ({date_str})"


class PartnershipRequest(models.Model):
    """Modèle pour les demandes de partenariat depuis la page de contact"""

    # Types de partenaires
    PARTNER_TYPES = [
        ('LIB', 'Librairie'),
        ('JV', 'Magasin Jeux Vidéo'),
        ('SUP', 'Superette'),
        ('CAF', 'Café'),
        ('BOO', 'Bouquinerie'),
        ('MAG', 'Magasin Général'),
        ('IND', 'Indépendant'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_name = models.CharField(max_length=255, verbose_name="Nom du commerce")
    business_type = models.CharField(
        max_length=3,
        choices=PARTNER_TYPES,
        verbose_name="Type de commerce"
    )
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    address = models.TextField(verbose_name="Adresse")
    message = models.TextField(verbose_name="Message")

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    is_processed = models.BooleanField(default=False, verbose_name="Traitée")

    class Meta:
        verbose_name = "Demande de partenariat"
        verbose_name_plural = "Demandes de partenariat"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.business_name} ({self.business_type}) - {self.email}"


# Alias pour compatibilité backwards - Library est maintenant Partner
Library = Partner
