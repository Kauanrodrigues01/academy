from datetime import timedelta, date, datetime
from django.test import TestCase
from django.utils.timezone import localdate
from parameterized import parameterized
from members.models import Member, Payment
from django.core.exceptions import ValidationError

class TestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Configuração inicial dos testes."""
        cls.member = Member.objects.create(
            email="test@example.com",
            full_name="Test User",
            phone="123456789"
        )

class MemberModelTestCase(TestBase):

    def test_member_creation(self):
        """Testa a criação de um membro."""
        self.assertEqual(self.member.email, "test@example.com")
        self.assertEqual(self.member.full_name, "Test User")
        self.assertFalse(self.member.is_active)
        
    def test_member_str(self):
        self.assertEqual(str(self.member), self.member.full_name)

    def test_last_payment_date_none(self):
        """Testa a propriedade last_payment_date sem pagamentos."""
        self.assertIsNone(self.member.last_payment_date)

    def test_last_payment_date(self):
        """Testa a propriedade last_payment_date com pagamentos."""
        Payment.objects.create(member=self.member, payment_date=localdate() - timedelta(days=5))
        Payment.objects.create(member=self.member, payment_date=localdate())
        self.assertEqual(self.member.last_payment_date, localdate())

    @parameterized.expand([
        (timedelta(days=15), True),  # Delta de 15 dias -> deve estar ativo
        (timedelta(days=31), False),  # Delta de 31 dias -> deve estar inativo
    ])
    def test_update_activity_status(self, delta_days, expected_status):
        """Testa o método update_activity_status com diferentes intervalos de pagamento."""
        Payment.objects.create(member=self.member, payment_date=localdate() - delta_days)
        self.member.update_activity_status()
        self.assertEqual(self.member.is_active, expected_status)


class PaymentModelTestCase(TestBase):

    def test_payment_creation(self):
        """Testa a criação de um pagamento."""
        payment = Payment.objects.create(member=self.member, amount=150.00)
        self.assertEqual(payment.member, self.member)
        self.assertEqual(payment.amount, 150.00)
        self.assertEqual(payment.payment_date, localdate())

    def test_payment_save_updates_member_status(self):
        """Testa se o método save do pagamento atualiza o status do membro."""
        self.assertFalse(self.member.is_active)
        payment = Payment.objects.create(member=self.member, amount=100.00, payment_date=localdate())
        self.member.refresh_from_db()
        self.assertTrue(self.member.is_active)
        
        payment.delete()
        self.assertTrue(self.member.is_active)
        payment = Payment.objects.create(member=self.member, amount=100.00, payment_date=localdate() - timedelta(days=31))
        self.assertFalse(self.member.is_active)

    def test_payment_str(self):
        """Testa o método __str__ do modelo Payment."""
        payment = Payment.objects.create(member=self.member, amount=100.00)
        self.assertEqual(str(payment), f"{self.member.full_name} | {payment.payment_date} | R$ {payment.amount}")

    def test_payment_str_no_member(self):
        """Testa o método __str__ do modelo Payment sem membro associado."""
        payment = Payment.objects.create(member=self.member, amount=100.00)
        self.member.delete()
        payment.refresh_from_db()
        self.assertEqual(
            str(payment), f"Pagamento sem aluno associado | {payment.payment_date} | R$ {payment.amount}"
        )

    @parameterized.expand([
        (1, 100.00),  # Mês with payment
        (2, 0.00),  # Mês without payment
    ])
    def test_get_monthly_profit(self, month, expected_total):
        """Testa o cálculo de lucros em um mês específico."""
        if month == 1:
            Payment.objects.create(member=self.member, amount=100.00, payment_date=datetime(2024, 1, 1))
        total_profit = Payment.get_monthly_profit(month=month)
        self.assertEqual(total_profit, expected_total)

    def test_get_monthly_profit_invalid_month(self):
        """Testa o comportamento ao passar um mês inválido."""
        with self.assertRaises(ValidationError):
            Payment.get_monthly_profit(month=13)

    def test_get_current_month_profit(self):
        """Testa o cálculo de lucros no mês atual."""
        Payment.objects.create(member=self.member, amount=100.00, payment_date=localdate())
        Payment.objects.create(member=self.member, amount=200.00, payment_date=localdate())
        total_profit = Payment.get_current_month_profit()
        self.assertEqual(total_profit, 300.00)
        
        Payment.objects.create(member=self.member, amount=200.00, payment_date=localdate())
        total_profit = Payment.get_current_month_profit()
        self.assertEqual(total_profit, 500.00)

    def test_get_current_year_profit(self):
        """Testa o cálculo de lucros no ano atual."""
        current_year = localdate().year
        january_date = date(current_year, 1, 10)
        july_date = date(current_year, 7, 10)
        
        Payment.objects.create(member=self.member, amount=100.00, payment_date=january_date)
        Payment.objects.create(member=self.member, amount=200.00, payment_date=july_date)
        
        total_profit = Payment.get_current_year_profit()
        self.assertEqual(total_profit, 300.00)