from django.test import TestCase
from django.urls import reverse
from users.models import User
from admin_panel.models import Member
from members.forms import MemberEditForm
from faker import Faker


class EditMemberViewAndEditMemberTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker('pt_BR')
        
        cls.password = cls.faker.password(length=12, upper_case=True, special_chars=True, digits=True)
        
        cls.user = User.objects.create_user(
            cpf=cls.faker.cpf().replace('.', '').replace('-', ''),
            email=cls.faker.email(),
            password=cls.password
        )
        
        cls.member = Member.objects.create(
            email="member@example.com",
            full_name="Test Member",
            phone="123456789",
            is_active=True,
        )
        cls.edit_member_url = reverse("admin_panel:edit_member", kwargs={'id': cls.member.id})
        cls.edit_member_view_url = reverse("admin_panel:edit_member_view", kwargs={'id': cls.member.id})
        cls.valid_data = {
            "email": "updated@example.com",  
            "full_name": "Updated Member",  
            "phone": "9876543210", 
            "is_active": False, 
        }
        cls.invalid_data = {
            "email": "invalid-email",
            "full_name": "",
            "phone": "",
            "is_active": False,
        }
    
    def test_edit_member_view_renders_correct_template(self):
        """Testa se a página de edição renderiza o template correto."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.edit_member_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_panel/pages/member_edit.html")

    def test_edit_member_view_contains_form_and_member(self):
        """Testa se o formulário e os dados do membro estão presentes no contexto."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.edit_member_view_url)
        self.assertIsInstance(response.context["form"], MemberEditForm)
        self.assertEqual(response.context["member"], self.member)
        
    def test_edit_member_view_renders_form_with_instance_member(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(self.edit_member_view_url)
        self.assertContains(response, self.member.email)
        self.assertContains(response, self.member.full_name)
        self.assertContains(response, self.member.phone)
        
    def test_edit_member_view_return_404_status_code_if_not_exists_member_with_id(self):
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(reverse("admin_panel:edit_member_view", kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
        
    def test_edit_member_view_loads_session_data(self):
        """Testa se os dados da sessão são usados para pré-popular o formulário."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        session_data = {
            'email': 'session@example.com',
            'full_name': 'Session Member',
            'phone': '111111111',
            'is_active': True
        }
        session = self.client.session
        session['form_data_edit_member'] = session_data
        session.save()

        response = self.client.get(self.edit_member_view_url)
        form = response.context['form']

        # Verifica se o formulário foi preenchido com os dados da sessão
        self.assertEqual(form.data['email'], session_data['email'])
        self.assertEqual(form.data['full_name'], session_data['full_name'])
        self.assertEqual(form.data['phone'], session_data['phone'])
        self.assertTrue(form.data['is_active'])


    def test_edit_member_successful_post(self):
        """Testa se a edição de membro funciona com dados válidos."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.post(self.edit_member_url, data=self.valid_data)
        
        member = Member.objects.get(id=self.member.id)
        self.assertEqual(member.email, self.valid_data['email'])
        self.assertEqual(member.full_name, self.valid_data['full_name'])
        self.assertEqual(member.phone, self.valid_data['phone'])
        self.assertFalse(member.is_active)
        self.assertRedirects(response, reverse("admin_panel:members"))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(messages[0].message, 'Membro atualizado com sucesso!')

    def test_edit_member_invalid_post(self):
        """Testa se a submissão de dados inválidos retorna os erros corretamente."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.post(self.edit_member_url, data=self.invalid_data)
        
        messages = list(response.wsgi_request._messages)
        self.assertEqual(messages[0].message, 'Erro ao atualizar o membro. Verifique os dados e tente novamente.')
        
        response = self.client.get(self.edit_member_view_url)
        form_errors = response.context['form'].errors
        self.assertIn('email', form_errors)
        self.assertIn('full_name', form_errors)
        self.assertIn('phone', form_errors)

    def test_edit_member_404_for_nonexistent_member(self):
        """Testa se acessar um membro inexistente retorna 404."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.get(reverse('admin_panel:edit_member', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_edit_member_session_data_persisted(self):
        """Testa se os dados do formulário inválido são armazenados na sessão."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        response = self.client.post(self.edit_member_url, data=self.invalid_data)
        session_data = response.wsgi_request.session.get("form_data_edit_member")
        self.assertIsNotNone(session_data)
        self.assertEqual(session_data["email"], "invalid-email")
        self.assertEqual(session_data["full_name"], "")
        self.assertEqual(session_data["phone"], "")

    def test_edit_member_clears_session_on_success(self):
        """Testa se os dados da sessão são removidos após uma submissão bem-sucedida."""
        self.client.login(cpf=self.user.cpf, password=self.password)
        session = self.client.session
        session["form_data_edit_member"] = self.valid_data
        session.save()

        self.client.post(self.edit_member_url, data=self.valid_data)
        session_data = self.client.session.get("form_data_edit_member")
        self.assertIsNone(session_data)
