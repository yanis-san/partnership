from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .models import Partner, Payment, PaymentReceipt, PartnershipRequest


def validate_image_size(file):
    """Valide que la taille de l'image est <= 5MB"""
    file_size = file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(
            f"L'image est trop grande. Max {limit_mb}MB, vous avez {file_size / (1024 * 1024):.1f}MB."
        )


class PartnerCreationForm(forms.ModelForm):
    """Formulaire de création rapide de partenaire par l'admin"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }),
        label="Mot de passe",
        help_text="Le mot de passe du compte partenaire"
    )

    class Meta:
        model = Partner
        fields = ('name', 'partner_type', 'email', 'phone', 'contact_person', 'address', 'commission_per_student')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du partenaire'
            }),
            'partner_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone (optionnel)'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Personne de contact'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse',
                'rows': 3
            }),
            'commission_per_student': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Commission par étudiant (DA)',
                'value': 1000
            }),
        }

    def save(self, commit=True):
        partner = super().save(commit=False)

        # Créer un compte utilisateur associé
        user = User.objects.create_user(
            username=partner.email,  # Utilise l'email comme username
            email=partner.email,
            password=self.cleaned_data['password']
        )
        partner.user = user

        if commit:
            partner.save()

        return partner


class QuickPaymentForm(forms.Form):
    """Formulaire simplifié pour ajouter rapidement un paiement avec reçu"""
    amount_paid = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Montant payé (DA)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0',
            'autofocus': 'autofocus'
        })
    )

    receipt_image = forms.ImageField(
        label="Photo du reçu",
        help_text="Max 5 MB - JPG, PNG ou JPEG",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'capture': 'environment',
            'required': True
        }),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ]
    )

    notes = forms.CharField(
        required=False,
        label="Notes (optionnel)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ex: Virement bancaire du 15/11/2024'
        })
    )


class PartnershipRequestForm(forms.ModelForm):
    """Formulaire pour les demandes de partenariat depuis la page de contact"""

    class Meta:
        model = PartnershipRequest
        fields = ['business_name', 'business_type', 'email', 'phone', 'address', 'message']
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: La Librairie du Centre'
            }),
            'business_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+213 XXX XX XX XX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '123 Rue de la Paix, Alger'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Parlez-nous de votre commerce et vos attentes...'
            }),
        }
        labels = {
            'business_name': 'Nom du commerce',
            'business_type': 'Type de commerce',
            'email': 'Email',
            'phone': 'Téléphone',
            'address': 'Adresse',
            'message': 'Message',
        }
