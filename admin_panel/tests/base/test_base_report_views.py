from django.test import TestCase
import pypdf
from io import BytesIO
from django.urls import reverse
from users.models import User
from django.utils.timezone import localdate
from members.models import Member, Payment
from faker import Faker

class TestBaseReportViews(TestCase):
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
            full_name='Active Member',
            email='active@example.com',
            is_active=True,
        )
        cls.member_inactive = Member.objects.create(
            full_name='Inactive Member',
            email='inactive@example.com',
            is_active=False,
        )
        
        Payment.objects.create(member=cls.member_active, amount=100.00, payment_date=localdate())
        Payment.objects.create(member=cls.member_active, amount=50.00, payment_date=localdate())
        
        cls.general_report_url = reverse('admin_panel:generate_pdf_general_report')
        cls.current_day_report_url = reverse('admin_panel:generate_pdf_report_of_current_day')
        
    def extract_text_from_pdf(self, pdf_content):
        '''Helper function to extract text from PDF content.'''
        with BytesIO(pdf_content) as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
        