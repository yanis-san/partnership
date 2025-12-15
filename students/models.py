from django.db import models
from partnerships.models import Partner
import uuid


class Program(models.Model):
    """Modèle pour les programmes/ateliers disponibles"""
    name = models.CharField(max_length=100, verbose_name="Nom du programme", unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    """Modèle pour les élèves inscrits"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Informations personnelles
    full_name = models.CharField(max_length=200, verbose_name="Nom complet", null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")

    # Référence partenaire
    partner = models.ForeignKey(
        Partner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Partenaire"
    )

    # Code utilisé lors de l'inscription
    referral_code = models.CharField(
        max_length=100,
        verbose_name="Code de parrainage utilisé",
        blank=True
    )

    # Informations d'inscription
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    # Programme/Atelier
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='students',
        verbose_name="Programme"
    )

    # Statut d'inscription
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

    # Confirmation de l'inscription par l'admin
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Inscription confirmée",
        help_text="Cochez pour confirmer l'inscription officielle (montant de 1000 DA acquis)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"
        ordering = ['-enrollment_date']

    def __str__(self):
        return self.full_name
