from django.test import TestCase
from django.urls import reverse
from users.models import User
from admin_panel.models import Payment, Member
from django.utils.timezone import localdate
from datetime import timedelta
from faker import Faker
from parameterized import parameterized

class FinanceViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker('pt_BR')

        cls.password = cls.faker.password(length=12, upper_case=True, special_chars=True, digits=True)

        cls.user = User.objects.create_user(
            cpf=cls.faker.cpf().replace('.', '').replace('-', ''),
            email=cls.faker.email(),
            password=cls.password
        )

        # Criação de um membro
        cls.member = Member.objects.create(
            email="member@example.com",
            full_name="John Doe",
            phone="123456789",
            start_date=localdate(),
            is_active=True
        )

        # Criação de pagamentos para todos os meses
        today = localdate()
        payments = []
        for month in range(1, 13):
            payment_date = today.replace(month=month, day=1)
            amount = month * 50  # Pagamento em incrementos de 50
            payments.append(Payment(member=cls.member, payment_date=payment_date, amount=amount))

        Payment.objects.bulk_create(payments)

        cls.finance_url = reverse('admin_panel:finance')

    def test_finance_view_requires_authentication(self):
        response = self.client.get(self.finance_url)
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(response.url.startswith(reverse('users:login_view')))

    def test_finance_view_renders_correctly(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('current_year_profit', response.context)
        self.assertIn('current_month_profit', response.context)
        self.assertIn('months_profit', response.context)
        self.assertIn('month_with_highest_profit', response.context)
        self.assertIn('recents_payments', response.context)
        self.assertIn('graph_html', response.context)

    def test_finance_view_current_year_profit(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        self.assertEqual(response.context['current_year_profit'], sum(range(50, 650, 50)))

    def test_finance_view_current_month_profit(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        current_month_amount = localdate().month * 50
        self.assertEqual(response.context['current_month_profit'], current_month_amount)
        
    @parameterized.expand([
        ('Janeiro',), ('Fevereiro',), ('Março',), ('Abril',), 
        ('Maio',), ('Junho',), ('Julho',), ('Agosto',),
        ('Setembro',), ('Outubro',), ('Novembro',), ('Dezembro',)
    ])
    def test_month_in_context(self, month):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        months_profit = response.context['months_profit']
        
        self.assertIn(month, months_profit)

    def test_finance_view_month_with_highest_profit(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        highest_month = 12
        month_names = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        self.assertEqual(response.context['month_with_highest_profit'], month_names[highest_month - 1])

    def test_finance_view_recent_payments(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        recent_payments = response.context['recents_payments']
        self.assertEqual(recent_payments.count(), 12)
        self.assertQuerySetEqual(
            recent_payments,
            Payment.objects.order_by('-payment_date')[:12],
            transform=lambda x: x
        )

    @parameterized.expand([
        ('Lucro Total do Ano', f'R$ {sum(range(50, 650, 50))}'),
        ('Lucro do Mês atual', f'R$ {localdate().month * 50}'),
        ('Mês com Maior Lucro', 'Dezembro'),
    ])
    def test_dashboard_cards_display_correct_data(self, card_title, expected_value):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        html = response.content.decode()

        self.assertIn(card_title, html)
        self.assertIn(expected_value, html)


    def test_finance_view_download_links(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        html = response.content.decode()
        self.assertIn(reverse('admin_panel:generate_pdf_general_report'), html)
        self.assertIn(reverse('admin_panel:generate_pdf_report_of_current_day'), html)

    @parameterized.expand([
        ('January', 50),
        ('February', 100),
        ('March', 150),
        ('April', 200),
        ('May', 250),
        ('June', 300),
        ('July', 350),
        ('August', 400),
        ('September', 450),
        ('October', 500),
        ('November', 550),
        ('December', 600),
    ])
    def test_monthly_profit_list_contains_correct_data(self, month, profit):
        """
        Testa se cada mês e seu lucro esperado estão presentes na lista <ul>.
        """
        months_in_portuguese = {
            'January': 'Janeiro',
            'February': 'Fevereiro',
            'March': 'Março',
            'April': 'Abril',
            'May': 'Maio',
            'June': 'Junho',
            'July': 'Julho',
            'August': 'Agosto',
            'September': 'Setembro',
            'October': 'Outubro',
            'November': 'Novembro',
            'December': 'Dezembro',
        }
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        html = response.content.decode('utf-8')

        expected_li = f"<li>{months_in_portuguese[month]} | R$ {profit}</li>"
        self.assertIn(expected_li, html)
        
    @parameterized.expand([
        ('Janeiro', 50), ('Fevereiro', 100), ('Março', 150), ('Abril', 200),
        ('Maio', 250), ('Junho', 300), ('Julho', 350), ('Agosto', 400),
        ('Setembro', 450), ('Outubro', 500), ('Novembro', 550), ('Dezembro', 600)
    ])
    def test_finance_view_graph_contains_correct_data(self, month, profit):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.finance_url)
        graph_html = response.context['graph_html']

        self.assertIn('Lucro Mensal', graph_html)
        if month != 'Março':
            self.assertIn(month, graph_html)
        self.assertIn(str(profit), graph_html)