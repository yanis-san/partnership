from django import forms
from .models import Student
from partnerships.models import PartnershipCode


class StudentRegistrationForm(forms.ModelForm):
    referral_code = forms.CharField(
        max_length=100,
        required=True,
        label="Code partenaire",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex. LIB4F6 ou JV9A2',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = Student
        fields = ('full_name', 'email', 'phone', 'program')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone (optionnel)'
            }),
            'program': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')

        if not referral_code:
            raise forms.ValidationError("Le code partenaire est requis.")

        # Vérifier si le code existe et est actif
        try:
            partnership = PartnershipCode.objects.get(
                code=referral_code.strip().upper(),
                is_active=True,
                partner__status='active'
            )
        except PartnershipCode.DoesNotExist:
            raise forms.ValidationError(
                "Code partenaire invalide ou inactif. Veuillez vérifier le code fourni par votre partenaire."
            )

        return referral_code.strip().upper()

    def save(self, commit=True):
        student = super().save(commit=False)
        referral_code = self.cleaned_data.get('referral_code')

        # Trouver le partenaire associé au code
        partnership = PartnershipCode.objects.get(code=referral_code)
        student.partner = partnership.partner
        student.referral_code = referral_code

        if commit:
            student.save()

        return student
