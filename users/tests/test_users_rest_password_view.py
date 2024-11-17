from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from unittest.mock import patch
from users.forms import PasswordResetRequestForm, PasswordResetForm
from django.utils.encoding import smart_bytes, smart_str


class PasswordResetViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Configura o usuário para os testes de redefinição de senha"""
        cls.user = get_user_model().objects.create_user(
            cpf='12345678901',
            email='user@example.com',
            password='password123'
        )
    
    def test_password_reset_view_get(self):
        """Testa se o formulário de redefinição de senha é exibido corretamente"""
        response = self.client.get(reverse('users:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Redefinir Senha')
        self.assertContains(response, '<input type="email" name="email"')
    
    def test_password_reset_send_valid_email(self):
        """Testa se o envio de um e-mail válido para redefinir a senha envia o link"""
        response = self.client.post(reverse('users:password_reset_send'), {
            'email': 'user@example.com'
        })
        self.assertRedirects(response, reverse('users:login_view'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Se o e-mail existir, um link para redefinir sua senha foi enviado.")
    
    def test_password_reset_send_invalid_email(self):
        """Testa se o envio de um e-mail inválido gera um erro"""
        response = self.client.post(reverse('users:password_reset_send'), {
            'email': 'nonexistent@example.com'
        })
        self.assertRedirects(response, reverse('users:password_reset'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Por favor, corrija os erros abaixo.')
    
    def test_password_reset_send_invalid_email_format(self):
        """Testa se o formato do e-mail inválido gera um erro"""
        response = self.client.post(reverse('users:password_reset_send'), {
            'email': 'invalidemail'
        })
        self.assertRedirects(response, reverse('users:password_reset'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Por favor, corrija os erros abaixo.')
    
    def test_password_reset_confirm_view_get(self):
        """Testa se o formulário de redefinição de senha com a nova senha é exibido corretamente"""
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        url = reverse('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nova Senha')
        self.assertContains(response, '<input type="password" name="password"')
    
    def test_password_reset_confirm_invalid_token(self):
        """Testa se o link de redefinição de senha com token inválido gera erro"""
        invalid_token = 'invalidtoken'
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        url = reverse('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': invalid_token})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('users:password_reset'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Link expirado ou inválido. Faça a solicitação novamente.')

    def test_password_reset_complete_valid(self):
        """Testa se a redefinição de senha é realizada com sucesso"""
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        url_view = reverse('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        url_complete = reverse('users:password_reset_complete')

        response = self.client.get(url_view)
        
        response = self.client.post(url_complete, {
            'password': 'NewPassword123',
            'password_confirm': 'NewPassword123'
        })
        self.assertRedirects(response, reverse('users:login_view'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Senha redefinida com sucesso!')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123'))

    def test_password_reset_complete_invalid_passwords(self):
        """Testa se a redefinição de senha falha se as senhas não coincidirem"""
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        url_view = reverse('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        url_complete = reverse('users:password_reset_complete')

        response = self.client.get(url_view)
        
        response = self.client.post(url_complete, {
            'password': 'NewPassword123',
            'password_confirm': 'DifferentPassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona de volta ao formulário
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Por favor, corrija os erros abaixo.')

    def test_password_reset_complete_invalid_password_format(self):
        """Testa se a redefinição de senha falha se a nova senha não atender aos requisitos de segurança"""
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        url_view = reverse('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        url_complete = reverse('users:password_reset_complete')

        response = self.client.get(url_view)

        response = self.client.post(url_complete, {
            'password': 'short',
            'password_confirm': 'short'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona de volta ao formulário
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Por favor, corrija os erros abaixo.')