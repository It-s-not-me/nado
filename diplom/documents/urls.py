from django.urls import path
from .views import (
    document_list,
    document_detail,
    document_create,
    document_file,
    required_document_status_update,
    staff_dashboard,
    staff_client_case_create,
    after_login_redirect,
)

urlpatterns = [
    path('', document_list, name='document_list'),

    path('after-login/', after_login_redirect, name='after_login_redirect'),

    path('staff/', staff_dashboard, name='staff_dashboard'),
    path('staff/client/create/', staff_client_case_create, name='staff_client_case_create'),

    path('document/<int:pk>/', document_detail, name='document_detail'),
    path('create/', document_create, name='document_create'),
    path('document/<int:pk>/file/', document_file, name='document_file'),

    path(
        'required-document/<int:pk>/status/',
        required_document_status_update,
        name='required_document_status_update'
    ),
]