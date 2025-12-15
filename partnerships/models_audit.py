"""
Modèles d'audit pour tracker les actions importantes du système.
Essentiels pour traçabilité et compliance.
"""
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """
    Log général pour toutes les actions importantes.
    Permet de tracer qui a fait quoi et quand.
    """

    ACTION_CHOICES = [
        ('student_registered', 'Étudiant inscrit'),
        ('student_confirmed', 'Étudiant confirmé'),
        ('student_rejected', 'Étudiant rejeté'),
        ('payment_created', 'Paiement créé'),
        ('payment_updated', 'Paiement mis à jour'),
        ('payment_completed', 'Paiement validé'),
        ('receipt_uploaded', 'Reçu uploadé'),
        ('partner_created', 'Partenaire créé'),
        ('partner_updated', 'Partenaire mis à jour'),
        ('code_generated', 'Code partenaire généré'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Action
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(help_text="Description détaillée de l'action")

    # Acteur
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='audit_logs', help_text="Utilisateur ayant effectué l'action")
    actor_email = models.EmailField(blank=True, help_text="Email de l'acteur (si pas de user)")

    # Entités impliquées
    student_id = models.UUIDField(null=True, blank=True, help_text="ID de l'étudiant impliqué")
    student_name = models.CharField(max_length=255, blank=True)
    student_email = models.EmailField(blank=True)

    partner_id = models.UUIDField(null=True, blank=True, help_text="ID du partenaire impliqué")
    partner_name = models.CharField(max_length=255, blank=True)

    payment_id = models.UUIDField(null=True, blank=True, help_text="ID du paiement impliqué")
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Données supplémentaires
    old_values = models.JSONField(null=True, blank=True,
                                  help_text="État précédent (pour modifications)")
    new_values = models.JSONField(null=True, blank=True,
                                  help_text="Nouvel état")

    # Métadonnées
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['student_id']),
            models.Index(fields=['partner_id']),
            models.Index(fields=['payment_id']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.get_action_display()} - {self.created_at}"

    @classmethod
    def log_student_confirmation(cls, student, user=None):
        """Log quand un étudiant est confirmé"""
        return cls.objects.create(
            action='student_confirmed',
            description=f"Étudiant {student.full_name} confirmé par {user}",
            user=user,
            student_id=student.id,
            student_name=student.full_name,
            student_email=student.email,
            partner_id=student.partner_id,
            partner_name=student.partner.name if student.partner else None,
            new_values={'is_confirmed': True, 'confirmed_at': str(__import__('django.utils.timezone', fromlist=['now']).now())}
        )

    @classmethod
    def log_payment_creation(cls, payment, user=None):
        """Log quand un paiement est créé"""
        return cls.objects.create(
            action='payment_created',
            description=f"Paiement de {payment.amount} DA créé pour {payment.partner.name}",
            user=user,
            partner_id=payment.partner_id,
            partner_name=payment.partner.name,
            payment_id=payment.id,
            payment_amount=payment.amount,
            new_values={'amount': str(payment.amount), 'status': payment.status}
        )

    @classmethod
    def log_payment_completion(cls, payment, user=None):
        """Log quand un paiement est marqué comme complété"""
        return cls.objects.create(
            action='payment_completed',
            description=f"Paiement {payment.id} validé pour {payment.partner.name}",
            user=user,
            partner_id=payment.partner_id,
            partner_name=payment.partner.name,
            payment_id=payment.id,
            payment_amount=payment.amount,
            old_values={'status': 'pending'},
            new_values={'status': 'completed', 'completed_at': str(__import__('django.utils.timezone', fromlist=['now']).now())}
        )

    @classmethod
    def log_receipt_upload(cls, receipt, user=None):
        """Log quand un reçu est uploadé"""
        return cls.objects.create(
            action='receipt_uploaded',
            description=f"Reçu uploadé pour paiement {receipt.payment_id}",
            user=user,
            payment_id=receipt.payment_id,
            payment_amount=receipt.amount_paid,
            new_values={'amount_paid': str(receipt.amount_paid), 'receipt_image': receipt.receipt_image.name}
        )
