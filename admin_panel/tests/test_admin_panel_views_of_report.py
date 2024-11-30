from django.test import TestCase
import PyPDF2
from io import BytesIO
from django.urls import reverse
from users.models import User
from django.utils.timezone import localdate
from members.models import Member, Payment
from faker import Faker
from unittest.mock import patch

class GeneratePDFGeneralReportTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the entire TestCase
        cls.faker = Faker('pt_BR')

        cls.password = cls.faker.password(length=12, upper_case=True, special_chars=True, digits=True)

        cls.user = User.objects.create_user(
            cpf=cls.faker.cpf().replace('.', '').replace('-', ''),
            email=cls.faker.email(),
            password=cls.password
        )
        
        cls.member_active = Member.objects.create(
            full_name="Active Member",
            email="active@example.com",
            is_active=True,
        )
        cls.member_inactive = Member.objects.create(
            full_name="Inactive Member",
            email="inactive@example.com",
            is_active=False,
        )
        cls.general_report_url = reverse('admin_panel:generate_pdf_general_report')
        Payment.objects.create(member=cls.member_active, amount=100.00, payment_date=localdate())
        Payment.objects.create(member=cls.member_active, amount=50.00, payment_date=localdate())
        
    def extract_text_from_pdf(self, pdf_content):
        """Helper function to extract text from PDF content."""
        with BytesIO(pdf_content) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
        
    def test_requires_authentication(self):
        # Ensure only authenticated users can access the view
        response = self.client.get(self.general_report_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertIn('/users/login/', response.url)

    def test_authenticated_access(self):
        # Log in and test access
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename=gym_report_'))

    def test_context_data(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)

        self.assertEqual(response.status_code, 200)
        pdf_content = self.extract_text_from_pdf(response.content)

        # Verify content in the PDF
        self.assertIn("R$150,00", pdf_content)  # Total revenue
        self.assertIn("Alunos Ativos: 1", pdf_content)
        self.assertIn("Alunos Pendentes: 1", pdf_content)

    def test_template_strings(self):
        # Check that template strings are present
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)
        pdf_content = self.extract_text_from_pdf(response.content)

        self.assertIn("Relatório Geral da Academia", pdf_content)
        self.assertIn("Resumo de Alunos", pdf_content)
        self.assertIn("Resumo da Receita", pdf_content)
        self.assertIn("Detalhes dos Pagamentos", pdf_content)

    def test_empty_payments(self):
        # Test behavior when there are no payments
        Payment.objects.all().delete()
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)
        pdf_content = self.extract_text_from_pdf(response.content)

        self.assertIn("R$0,00", pdf_content)  # Total revenue should be zero

    def test_multiple_members(self):
        # Test with multiple active and inactive members
        Member.objects.create(full_name="Another Active Member", email="active2@example.com", is_active=True)
        Member.objects.create(full_name="Another Inactive Member", email="inactive2@example.com", is_active=False)
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)
        pdf_content = self.extract_text_from_pdf(response.content)

        self.assertIn("Alunos Ativos: 2", pdf_content)
        self.assertIn("Alunos Pendentes: 2", pdf_content)

    def test_large_revenue(self):
        # Test behavior with large payments
        Payment.objects.create(member=self.member_active, amount=900.99, payment_date=localdate())
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)
        pdf_content = self.extract_text_from_pdf(response.content)

        self.assertIn("R$1050,99", pdf_content)  # Total revenue

    def test_invalid_methods(self):
        # Test unsupported HTTP methods
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.post(self.general_report_url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        response = self.client.put(self.general_report_url)
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(self.general_report_url)
        self.assertEqual(response.status_code, 405)
        
    @patch('admin_panel.views.pisa.CreatePDF')
    def test_error_in_pdf_generation(self, mock_create_pdf):
        mock_create_pdf.return_value.err = True
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.general_report_url)
        
        messages = list(response.wsgi_request._messages)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro ao gerar o PDF.')