from django.test import TestCase
from users.forms import LoginForm, PasswordResetRequestForm, PasswordResetForm
from django.contrib.auth import get_user_model
from utils import is_valid_cpf
from faker import Faker
from users.tests.base.test_base import TestBase

class LoginFormTests(TestBase):

    def test_valid_form(self):
        """Testa se o formulário é válido quando o CPF e a senha são corretos"""
        faker = Faker('pt_BR')
        form_data = {'cpf': self.valid_cpf, 'password': self.password}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_cpf_format(self):
        """Testa se o CPF está no formato correto"""
        form_data = {'cpf': self.invalid_cpf, 'password': self.password}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['cpf'], ['O CPF fornecido é inválido.'])

    def test_invalid_cpf_digits(self):
        """Testa se o CPF possui 11 dígitos"""
        form_data = {'cpf': '1234567890A', 'password': 'ValidPassword123'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['cpf'], ['O CPF fornecido é inválido.'])

    def test_invalid_cpf_check(self):
        """Testa se o CPF é válido segundo a função is_valid_cpf"""
        form_data = {'cpf': '12345678900', 'password': 'ValidPassword123'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['cpf'], ['O CPF fornecido é inválido.'])

    def test_missing_password(self):
        """Testa se o campo senha é obrigatório"""
        form_data = {'cpf': '12345678901'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)


class PasswordResetRequestFormTests(TestBase):

    def test_valid_email(self):
        """Testa se o formulário aceita um e-mail válido"""
        form_data = {'email': self.email}
        form = PasswordResetRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_format(self):
        """Testa se o formulário rejeita um e-mail inválido"""
        form_data = {'email': 'invalid-email'}
        form = PasswordResetRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Informe um endereço de email válido.'])

    def test_email_not_registered(self):
        """Testa se o formulário rejeita e-mail não registrado"""
        form_data = {'email': 'nonexistent@example.com'}
        form = PasswordResetRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Este e-mail não está registrado. Verifique novamente.'])

    def test_missing_email(self):
        """Testa se o campo de e-mail é obrigatório"""
        form_data = {}
        form = PasswordResetRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        

class PasswordResetFormTests(TestCase):

    def test_valid_password(self):
        """Testa se o formulário aceita uma senha válida"""
        form_data = {'password': 'NewPassword123', 'password_confirm': 'NewPassword123'}
        form = PasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        """Testa se o formulário rejeita senhas que não coincidem"""
        form_data = {'password': 'NewPassword123', 'password_confirm': 'DifferentPassword123'}
        form = PasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password_confirm'], ['As senhas não coincidem.'])

    def test_short_password(self):
        """Testa se o formulário rejeita senhas com menos de 6 caracteres"""
        form_data = {'password': 'Abcd1', 'password_confirm': 'Abcd1'}
        form = PasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['A senha deve ter pelo menos 6 caracteres.'])

    def test_missing_uppercase(self):
        """Testa se o formulário rejeita senhas sem letras maiúsculas"""
        form_data = {'password': 'password123', 'password_confirm': 'password123'}
        form = PasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['A senha deve conter pelo menos uma letra maiúscula.'])

    def test_missing_number(self):
        """Testa se o formulário rejeita senhas sem números"""
        form_data = {'password': 'Password!', 'password_confirm': 'Password!'}
        form = PasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['A senha deve conter pelo menos um número.'])

    def test_valid_password_special_characters(self):
        """Testa se o formulário aceita senhas com caracteres especiais"""
        form_data = {'password': '@#$%ValidPassword123!', 'password_confirm': '@#$%ValidPassword123!'}
        form = PasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

