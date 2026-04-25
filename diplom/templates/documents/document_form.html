from django import forms
from django.contrib.auth.models import User

from .models import Document, ServiceType


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
        labels = {
            'file': 'Файл',
        }


class StaffClientCaseForm(forms.Form):
    inn = forms.CharField(
        label='ИНН клиента',
        max_length=12,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ИНН клиента'
        })
    )

    full_name = forms.CharField(
        label='ФИО клиента',
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ФИО клиента'
        })
    )

    username = forms.CharField(
        label='Логин для клиента',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: client_ivanov'
        })
    )

    password = forms.CharField(
        label='Пароль для клиента',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        })
    )

    service_type = forms.ModelChoiceField(
        label='Тип услуги',
        queryset=ServiceType.objects.all()
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')

        return username