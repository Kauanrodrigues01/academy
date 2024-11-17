from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker

class TestBase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker('pt_BR')
        
        cls.valid_cpf = cls.faker.cpf().replace('.', '').replace('-', '')
        cls.invalid_cpf = '12345678901'
        
        cls.email = cls.faker.email()
        cls.full_name = cls.faker.name()
        cls.password = cls.faker.password(length=12, upper_case=True, special_chars=True, digits=True)
        
        cls.user_data = {
            'cpf': cls.valid_cpf,
            'email': cls.faker.email(domain='@exemple.com'),
            'full_name': cls.full_name,
            'password': cls.password,
        }        
        
        # Cria um usuário válido para os testes de login
        cls.user = get_user_model().objects.create_user(
            cpf=cls.faker.cpf().replace('.', '').replace('-', ''),
            email=cls.email,
            password=cls.password
        )