from members.tests.base.test_base_form import BaseTestCase
from django.utils.timezone import localdate
from datetime import timedelta
from members.forms import MemberPaymentForm, MemberEditForm, PaymentForm
from members.models import Member, Payment
from django.core.exceptions import ValidationError


class MemberPaymentFormTests(BaseTestCase):

    def test_valid_form(self):
        form = MemberPaymentForm(data=self.member_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_duplicate(self):
        Member.objects.create(email=self.member_data['email'], full_name=self.member_data['full_name'], phone=self.member_data['phone'])
        form = MemberPaymentForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Este e-mail já está cadastrado.'])
        
    def test_without_full_name(self):
        del self.member_data['full_name']
        form = MemberPaymentForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['O nome completo é obrigatório.'])
        
    def test_full_name_less_than_3_caracters(self):
        self.member_data['full_name'] = 'ad'
        form = MemberPaymentForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['O nome completo deve ter pelo menos 3 caracteres.'])
        
    def test_full_name_greater_than_50_caracters(self):
        self.member_data['full_name'] = 'a' * 51
        form = MemberPaymentForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['O nome completo deve ter menos de 50 caracteres.'])

    def test_invalid_phone(self):
        data = self.member_data.copy()
        data['phone'] = '12345' 
        form = MemberPaymentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'], ['O telefone deve conter apenas números e ter entre 10 e 15 dígitos.'])

    def test_payment_date_in_future(self):
        data = self.member_data.copy()
        data['payment_date'] = localdate() + timedelta(days=1)  # Data futura
        form = MemberPaymentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['payment_date'], ['A data de pagamento não pode ser no futuro.'])

    def test_save_method_creates_member_and_payment(self):
        Member.objects.all().delete()
        form = MemberPaymentForm(data=self.member_data)
        self.assertTrue(form.is_valid())
        member = form.save()
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.first().member, member)


class MemberEditFormTests(BaseTestCase):

    def test_valid_form(self):
        data = {
            'full_name': 'Novo Nome',
            'email': self.member.email,
            'phone': self.member.phone,
            'is_active': False
        }
        form = MemberEditForm(data=data, instance=self.member)
        self.assertTrue(form.is_valid())

    def test_invalid_form_duplicate_email(self):
        other_member = Member.objects.create(
            email=self.fake.email(),
            full_name=self.fake.name(),
            phone=self.fake.phone_number(),
            is_active=True
        )
        data = {
            'full_name': 'Novo Nome',
            'email': other_member.email,  # Email duplicado
            'phone': self.member.phone,
            'is_active': False
        }
        form = MemberEditForm(data=data, instance=self.member)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Já existe um aluno com este e-mail.'])
        
    def test_without_full_name(self):
        del self.member_data['full_name']
        form = MemberEditForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['O nome completo é obrigatório.'])
        
    def test_full_name_less_than_3_caracters(self):
        self.member_data['full_name'] = 'ad'
        form = MemberEditForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['O nome completo deve ter pelo menos 3 caracteres.'])
        
    def test_full_name_greater_than_50_caracters(self):
        self.member_data['full_name'] = 'a' * 51
        form = MemberPaymentForm(data=self.member_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['O nome completo deve ter menos de 50 caracteres.'])

    def test_invalid_phone(self):
        data = {
            'full_name': 'Novo Nome',
            'email': self.member.email,
            'phone': '12345',  # Telefone inválido
            'is_active': False
        }
        form = MemberEditForm(data=data, instance=self.member)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'], ['O telefone deve conter apenas números e ter entre 10 e 15 dígitos.'])


class PaymentFormTests(BaseTestCase):

    def test_valid_form(self):
        form = PaymentForm(data=self.payment_data)
        self.assertTrue(form.is_valid())

    def test_payment_date_in_future(self):
        data = self.payment_data.copy()
        data['payment_date'] = localdate() + timedelta(days=1)  # Data futura
        form = PaymentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['payment_date'], ['A data de pagamento não pode ser no futuro.'])

    def test_save_method_creates_payment(self):
        form = PaymentForm(data=self.payment_data)
        self.assertTrue(form.is_valid())
        payment = form.save(member=self.member)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(payment.member, self.member)
        
    def test_save_method_without_member(self):
        form = PaymentForm(data=self.payment_data)
        self.assertTrue(form.is_valid())
        
        with self.assertRaises(ValidationError):
            form.save()
            
    def test_save_method_commit_false_does_not_save_payment(self):
        form = PaymentForm(data=self.payment_data)
        self.assertTrue(form.is_valid())
        
        payment = form.save(member=self.member, commit=False)
        self.assertEqual(Payment.objects.count(), 0)
        
        payment.save()
        self.assertEqual(Payment.objects.count(), 1)
