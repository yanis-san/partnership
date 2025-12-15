from django.test import TestCase
from partnerships.models import Partner, PartnershipCode, Payment
from students.models import Student, Program
from decimal import Decimal


def create_completed_payment(partner, amount):
    """Helper: Create a completed payment"""
    return Payment.objects.create(
        partner=partner,
        amount=amount,
        remaining_amount=Decimal('0.00')
    )


def create_pending_payment(partner, amount):
    """Helper: Create a pending payment"""
    return Payment.objects.create(
        partner=partner,
        amount=amount,
        remaining_amount=amount
    )


class PartnerCommissionTests(TestCase):
    """Tests pour les calculs de commission"""

    def setUp(self):
        self.program = Program.objects.create(name="Test Program")
        self.partner = Partner.objects.create(
            name="Test Library",
            email="test@lib.com",
            commission_per_student=Decimal('1000.00'),
            status='active'
        )

    def test_single_student_commission(self):
        """Test la commission pour un seul étudiant"""
        Student.objects.create(
            full_name="Student 1",
            email="s1@test.com",
            partner=self.partner,
            program=self.program,
            is_confirmed=True
        )
        self.assertEqual(self.partner.total_earned, Decimal('1000.00'))

    def test_multiple_students_commission(self):
        """Test la commission pour plusieurs étudiants"""
        for i in range(5):
            Student.objects.create(
                full_name=f"Student {i}",
                email=f"s{i}@test.com",
                partner=self.partner,
                program=self.program,
                is_confirmed=True
            )
        self.assertEqual(self.partner.total_earned, Decimal('5000.00'))

    def test_commission_only_for_confirmed_students(self):
        """Test que seuls les étudiants confirmés comptent"""
        for i in range(3):
            Student.objects.create(
                full_name=f"Confirmed {i}",
                email=f"conf{i}@test.com",
                partner=self.partner,
                program=self.program,
                is_confirmed=True
            )
        for i in range(2):
            Student.objects.create(
                full_name=f"Unconfirmed {i}",
                email=f"unconf{i}@test.com",
                partner=self.partner,
                program=self.program,
                is_confirmed=False
            )

        self.assertEqual(self.partner.total_earned, Decimal('3000.00'))

    def test_remaining_balance(self):
        """Test le calcul du solde restant"""
        for i in range(10):
            Student.objects.create(
                full_name=f"Student {i}",
                email=f"st{i}@test.com",
                partner=self.partner,
                program=self.program,
                is_confirmed=True
            )

        create_completed_payment(self.partner, Decimal('4000.00'))

        expected_balance = Decimal('10000.00') - Decimal('4000.00')
        self.assertEqual(self.partner.remaining_balance, expected_balance)

    def test_payment_status_not_paid(self):
        """Test le statut quand aucun paiement"""
        Student.objects.create(
            full_name="Student 1",
            email="s1test@test.com",
            partner=self.partner,
            program=self.program,
            is_confirmed=True
        )
        self.assertEqual(self.partner.payment_status, "Non payé")

    def test_payment_status_partial(self):
        """Test le statut de paiement partiel"""
        for i in range(5):
            Student.objects.create(
                full_name=f"Student {i}",
                email=f"partial{i}@test.com",
                partner=self.partner,
                program=self.program,
                is_confirmed=True
            )

        create_completed_payment(self.partner, Decimal('3000.00'))
        self.assertEqual(self.partner.payment_status, "Partiel")

    def test_payment_status_fully_paid(self):
        """Test le statut quand complètement payé"""
        for i in range(5):
            Student.objects.create(
                full_name=f"Student {i}",
                email=f"paid{i}@test.com",
                partner=self.partner,
                program=self.program,
                is_confirmed=True
            )

        create_completed_payment(self.partner, Decimal('5000.00'))
        self.assertEqual(self.partner.payment_status, "Payé")


class PaymentModelTests(TestCase):
    """Tests du modèle Payment"""

    def setUp(self):
        self.partner = Partner.objects.create(
            name="Test",
            email="test@test.com",
            status='active'
        )

    def test_pending_payment(self):
        """Test création d'un paiement en attente"""
        payment = create_pending_payment(self.partner, Decimal('5000.00'))
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'pending')

    def test_completed_payment(self):
        """Test création d'un paiement complété"""
        payment = create_completed_payment(self.partner, Decimal('5000.00'))
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'completed')

