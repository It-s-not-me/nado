from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'status']
        labels = {
            'title': 'Название документа',
            'description': 'Описание',
            'file': 'Файл',
            'status': 'Статус',
        }