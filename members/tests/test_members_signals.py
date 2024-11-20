from django.test import TestCase
from datetime import timedelta
from members.models import Member, Payment
from django.utils.timezone import localdate
from unittest.mock import patch


class MemberSignalsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.member_data = {
            'email': 'teste@teste.com',
            'full_name': 'Aluno Teste',
            'phone': '5585966667843',
            'is_active': True
        }

    @patch('admin_panel.models.ActivityLog.objects.create')
    def test_member_creation_signal(self, mock_create):
        """Testa o sinal de criação de membro"""
        member = Member.objects.create(**self.member_data)
        self.assertEqual(mock_create.call_count, 1)
        self.assertIn(f'{member.full_name} foi cadastrado', mock_create.call_args[1]['description'])

    @patch('admin_panel.models.ActivityLog.objects.create')
    def test_member_update_signal(self, mock_create):
        """Testa o sinal de atualização de membro"""
        member = Member.objects.create(**self.member_data)
        member.full_name = 'Aluno Teste Atualizado'
        member.save()
        self.assertEqual(mock_create.call_count, 2)
        self.assertIn(f'{member.full_name} foi atualizado', mock_create.call_args[1]['description'])

    @patch('admin_panel.models.ActivityLog.objects.create')
    def test_member_delete_signal(self, mock_create):
        """Testa o sinal de exclusão de membro"""
        member = Member.objects.create(**self.member_data)
        member.delete()
        self.assertEqual(mock_create.call_count, 2)
        self.assertIn(f'{member.full_name} foi excluído', mock_create.call_args[1]['description'])


class PaymentSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = Member.objects.create(
            email='teste@teste.com',
            full_name='Aluno Teste',
            phone='5585966667843',
            is_active=True
        )
        cls.payment_data = {
            'payment_date': localdate(),
            'amount': 100.00
        }
        cls.payment_update = Payment.objects.create(member=cls.member, **cls.payment_data)

    @patch('admin_panel.models.ActivityLog.objects.create')
    @patch('members.models.Member.update_activity_status')
    def test_payment_creation_signal(self, mock_update_status, mock_create):
        """
        Testa o sinal de criação de pagamento. Este teste verifica se, 
        ao criar um pagamento, o método de atualização de status do 
        membro é chamado corretamente e se o log de atividade é registrado.
        
        O teste é dividido em dois aspectos principais:
        1. Verificar se o método `update_activity_status` foi chamado quando o pagamento foi criado.
        2. Verificar se o `ActivityLog.objects.create` foi chamado com a descrição correta do pagamento.
        """
        
        Payment.objects.create(member=self.member, **self.payment_data)
        
        mock_update_status.assert_called_once()
        
        self.assertEqual(mock_create.call_count, 1)
        self.assertIn('realizou um pagamento de R$ 100.0', mock_create.call_args[1]['description'])


    @patch('admin_panel.models.ActivityLog.objects.create')
    def test_payment_without_member(self, mock_create):
        """Testa o sinal de pagamento sem um membro associado"""
        Payment.objects.create(amount=100.00, payment_date=localdate())
        self.assertEqual(mock_create.call_count, 1)
        self.assertIn('Pagamento sem aluno associado | realizou um pagamento de R$ 100.0', mock_create.call_args[1]['description'])
        
    @patch('admin_panel.models.ActivityLog.objects.create')
    @patch('members.models.Member.update_activity_status')
    def test_payment_update_signal(self, mock_update_status, mock_create):
        """Testa o sinal de atualização de pagamento (não deve criar ActivityLog para pagamento)."""
        
        
        # Atualiza algum campo do pagamento (por exemplo, a data de pagamento)
        self.payment_update.payment_date = localdate() - timedelta(days=1)
        self.payment_update.save()  # Isso deve disparar o post_save, mas `created` será False
        
        # Verifica que o log de atividade **não** foi criado para o pagamento
        mock_create.assert_not_called()  # Nenhuma chamada ao create de ActivityLog para pagamento
        
        # Verifica que o log de atividade para o membro foi chamado
        mock_update_status.assert_called_once()  # O método update_activity_status foi chamado para o membro


