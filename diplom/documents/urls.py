from django.urls import path
from .views import document_list, document_detail, document_create

urlpatterns = [
    path('', document_list, name='document_list'),
    path('document/<int:pk>/', document_detail, name='document_detail'),
    path('create/', document_create, name='document_create'),
]