from django import forms
from .models import Member
import re

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_name', 'email', 'phone', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'id': 'student-name',
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'id': 'student-email',
                'class': 'form-control',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'id': 'student-phone',
                'class': 'form-control',
                'placeholder': 'Digite apenas números',
                'required': True
            }),
            'is_active': forms.Select(attrs={
                'id': 'student-status',
                'class': 'form-control',
            }, choices=[(True, 'Ativo'), (False, 'Inativo')]),
        }
        labels = {
            'full_name': 'Nome Completo',
            'email': 'E-mail',
            'phone': 'Telefone',
            'is_active': 'Status'
        }

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not full_name:
            raise forms.ValidationError("O nome completo é obrigatório.")
        if len(full_name) < 3:
            raise forms.ValidationError("O nome completo deve ter pelo menos 3 caracteres.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\d{10,15}$', phone):
            raise forms.ValidationError("O telefone deve conter apenas números e ter entre 10 e 15 dígitos.")
        return phone

    def clean_is_active(self):
        is_active = self.cleaned_data['is_active']
        return is_active


class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_name', 'email', 'phone', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'id': 'student-name',
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'id': 'student-email',
                'class': 'form-control',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'id': 'student-phone',
                'class': 'form-control',
                'placeholder': 'Digite apenas números',
                'required': True
            }),
            'is_active': forms.Select(attrs={
                'id': 'student-status',
                'class': 'form-control',
            }, choices=[(True, 'Ativo'), (False, 'Inativo')]),
        }
        labels = {
            'full_name': 'Nome Completo',
            'email': 'E-mail',
            'phone': 'Telefone',
            'is_active': 'Status'
        }

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not full_name:
            raise forms.ValidationError("O nome completo é obrigatório.")
        if len(full_name) < 3:
            raise forms.ValidationError("O nome completo deve ter pelo menos 3 caracteres.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\d{10,15}$', phone):
            raise forms.ValidationError("O telefone deve conter apenas números e ter entre 10 e 15 dígitos.")
        return phone

    def clean_is_active(self):
        is_active = self.cleaned_data['is_active']
        return is_active