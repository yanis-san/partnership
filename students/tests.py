from django.test import TestCase
from students.models import Student, Program
from students.forms import StudentRegistrationForm
from partnerships.models import Partner, PartnershipCode


class StudentRegistrationFormTests(TestCase):
    """Tests du formulaire d'inscription d'étudiants"""

    def setUp(self):
        self.program = Program.objects.create(name="Python Course")
        self.partner = Partner.objects.create(
            name="Tech Library",
            email="tech@lib.com",
            status='active'
        )
        self.code = PartnershipCode.objects.create(
            partner=self.partner,
            code="LIB4F6",
            is_active=True
        )

    def test_valid_form(self):
        """Test le formulaire avec données valides"""
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '0541234567',
            'program': self.program.id,
            'referral_code': 'LIB4F6'
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_referral_code(self):
        """Test sans code de parrainage"""
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'program': self.program.id,
            'referral_code': ''
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_referral_code(self):
        """Test avec code invalide"""
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'program': self.program.id,
            'referral_code': 'INVALID123'
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_inactive_partner(self):
        """Test avec partenaire inactif"""
        inactive_partner = Partner.objects.create(
            name="Inactive",
            email="inactive@lib.com",
            status='inactive'
        )
        inactive_code = PartnershipCode.objects.create(
            partner=inactive_partner,
            code="INACT001",
            is_active=True
        )

        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'program': self.program.id,
            'referral_code': 'INACT001'
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        """Test que le formulaire enregistre correctement"""
        form_data = {
            'full_name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone': '0549876543',
            'program': self.program.id,
            'referral_code': 'LIB4F6'
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

        student = form.save()

        self.assertEqual(student.full_name, 'Jane Smith')
        self.assertEqual(student.email, 'jane@example.com')
        self.assertEqual(student.partner, self.partner)
        self.assertEqual(student.referral_code, 'LIB4F6')

    def test_code_case_insensitive(self):
        """Test que le code accepte les minuscules"""
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'program': self.program.id,
            'referral_code': 'lib4f6'
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_code_with_spaces(self):
        """Test que les espaces sont supprimés"""
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'program': self.program.id,
            'referral_code': '  LIB4F6  '
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

        student = form.save()
        self.assertEqual(student.referral_code, 'LIB4F6')

