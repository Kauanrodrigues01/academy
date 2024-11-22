from django.test import TestCase
from django.urls import reverse
from users.models import User
from django.utils.timezone import localdate
from members.models import Member, Payment
from datetime import timedelta
from faker import Faker


class TestMembersView(TestCase):
    def setUp(self):
        self.faker = Faker('pt_BR')
        
        self.password = self.faker.password(length=12, upper_case=True, special_chars=True, digits=True)
        
        self.user = User.objects.create_user(
            cpf=self.faker.cpf().replace('.', '').replace('-', ''),
            email=self.faker.email(),
            password=self.password
        )
        
        # Criar alguns membros para os testes
        self.member1 = Member.objects.create(
            full_name='John Doe',
            email='john@example.com',
            phone='123456789',
            is_active=True,
            start_date=localdate() - timedelta(days=30)
        )
        
        self.member2 = Member.objects.create(
            full_name='Jane Smith',
            email='jane@example.com',
            phone='987654321',
            is_active=False,
            start_date=localdate() - timedelta(days=60)
        )

        # Criar pagamentos para os membros
        self.payment_member1 = Payment.objects.create(member=self.member1, payment_date=localdate() - timedelta(days=10), amount=100)
        self.payment_member2 = Payment.objects.create(member=self.member2, payment_date=localdate() - timedelta(days=40), amount=100)

        self.members_url = reverse('admin_panel:members')
        self.login_url = reverse('users:login_view')

    def test_authenticated_user_can_access_page(self):
        # Testar se o usuário autenticado pode acessar a página
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.members_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/pages/members.html')
    
    def test_unauthenticated_user_redirected(self):
        # Testar se o usuário não autenticado é redirecionado para a página de login
        response = self.client.get(self.members_url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_search_filter(self):
        # Testar a funcionalidade de filtro de busca
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.members_url, {'q': 'John'})
        content = response.content.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.member1.full_name, content)
        self.assertNotIn(self.member2.full_name, content)

    def test_status_filter(self):
        # Testar a filtragem por status (ativos/inativos)
        self.client.login(cpf=self.user.cpf, password=self.password)
        
        # Testar membros ativos
        response = self.client.get(self.members_url, {'status': 'active'})
        content = response.content.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.member1.full_name, content)
        self.assertNotIn(self.member2.full_name, content)
        
        # Testar membros inativos
        response = self.client.get(self.members_url, {'status': 'inactive'})
        content = response.content.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.member2.full_name, content)
        self.assertNotIn(self.member1.full_name, content)

    def test_payment_date_filter(self):
        # Testar o filtro por data de pagamento
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.members_url, {'last_payment': self.payment_member1.payment_date})
        content = response.content.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.member1.full_name, content)
        self.assertNotIn(self.member2.full_name, content)

    def test_pagination(self):
        # Testar a paginação
        self.client.login(cpf=self.user.cpf, password=self.password)
        
        # Criar mais membros para testar a paginação
        for i in range(20, 31):
            Member.objects.create(
                full_name=f'Member {i}',
                email=f'member{i}@example.com',
                phone=f'1234567{i}',
                is_active=True,
                start_date=localdate() - timedelta(days=i)
            )
        
        response = self.client.get(self.members_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1')  # Verificar se a página 1 aparece
        self.assertContains(response, '2')  # Verificar se a página 2 aparece
        
        # Verificar membros na página 1
        for i in range(20, 31):
            self.assertContains(response, f'Member {i}')
        

    def test_context_data(self):
        # Testar o contexto da view
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.members_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('members', response.context)
        self.assertIn('pagination_range', response.context)
        self.assertIn('search_query', response.context)
        self.assertIn('form', response.context)

    def test_no_members_found(self):
        # Testar quando nenhum membro é encontrado
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.members_url, {'q': 'Nonexistent Name'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum aluno encontrado.')

    def test_edge_case_with_few_members(self):
        # Testar com poucos membros (menos que 10)
        self.client.login(cpf=self.user.cpf, password=self.password)
        
        # Criar 5 membros
        for i in range(1, 6):
            Member.objects.create(
                full_name=f'Member {i}',
                email=f'member{i}@example.com',
                phone=f'1234567{i}',
                is_active=True,
                start_date=localdate() - timedelta(days=i)
            )

        response = self.client.get(self.members_url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que todos os membros estão na página, sem necessidade de paginação
        for i in range(1, 6):
            self.assertContains(response, f'Member {i}')
        
        # Verificar que não há links para páginas adicionais
        self.assertNotContains(response, 'Next')
        self.assertNotContains(response, 'Previous')

    def test_no_results_for_filter(self):
        # Testar quando um filtro não retorna resultados
        self.client.login(cpf=self.user.cpf, password=self.password)
        self.member1.delete()
        
        response = self.client.get(self.members_url, {'status': 'active'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum aluno encontrado.')
        
    def test_form_add_member(self):
        # Testar se o formulário de adicionar membro está funcionando
        self.client.login(cpf=self.user.cpf, password=self.password)
        
        # Testando a view com o formulário
        response = self.client.get(self.members_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
