from django import forms
from django.contrib.auth.models import User

from .models import Document, ServiceType, ClientCase, Feedback


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
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: client_ivanov'
        })
    )

    password = forms.CharField(
        label='Пароль для клиента',
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        })
    )

    service_type = forms.ModelChoiceField(
        label='Тип услуги',
        queryset=ServiceType.objects.all()
    )

    organization_name = forms.CharField(
        label='Полное название организации',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Акционерное общество «Ромашка»'
        })
    )

    short_organization_name = forms.CharField(
        label='Сокращённое название организации',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: АО «Ромашка»'
        })
    )

    legal_address = forms.CharField(
        label='Юридический адрес',
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите юридический адрес'
        })
    )

    director_full_name = forms.CharField(
        label='ФИО руководителя',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ФИО руководителя'
        })
    )

    authorized_capital = forms.CharField(
        label='Уставный капитал',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: 100 000 рублей'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')

        return username

    def clean(self):
        cleaned_data = super().clean()
        inn = cleaned_data.get('inn')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        from .models import Client
        client_exists = Client.objects.filter(inn=inn).exists()

        if not client_exists:
            if not username:
                self.add_error('username', 'Для нового клиента нужно указать логин.')
            if not password:
                self.add_error('password', 'Для нового клиента нужно указать пароль.')

        return cleaned_data


class ClientCaseEditForm(forms.ModelForm):
    class Meta:
        model = ClientCase
        fields = [
            'organization_name',
            'short_organization_name',
            'legal_address',
            'director_full_name',
            'authorized_capital',
            'is_complete',
        ]
        labels = {
            'organization_name': 'Полное название организации',
            'short_organization_name': 'Сокращённое название организации',
            'legal_address': 'Юридический адрес',
            'director_full_name': 'ФИО руководителя',
            'authorized_capital': 'Уставный капитал',
            'is_complete': 'Комплект документов собран',
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'message']
        labels = {
            'title': 'Тема',
            'message': 'Описание проблемы',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: не загружается документ'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Опишите, что произошло и на какой странице',
                'rows': 6
            }),
        }