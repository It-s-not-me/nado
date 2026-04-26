from django.urls import path
from .views import (
    document_list,
    document_detail,
    document_create,
    document_file,
    document_delete,
    required_document_status_update,
    staff_dashboard,
    staff_client_case_create,
    after_login_redirect,
    generate_charter,
    staff_client_case_edit,
    document_replace,
    staff_client_case_detail,
    feedback_create,
)

urlpatterns = [
    path('', document_list, name='document_list'),
    path('after-login/', after_login_redirect, name='after_login_redirect'),

    path('staff/', staff_dashboard, name='staff_dashboard'),
    path('staff/client/create/', staff_client_case_create, name='staff_client_case_create'),
    path('staff/case/<int:pk>/edit/', staff_client_case_edit, name='staff_client_case_edit'),

    path('document/<int:pk>/', document_detail, name='document_detail'),
    path('document/<int:pk>/file/', document_file, name='document_file'),
    path('document/<int:pk>/delete/', document_delete, name='document_delete'),
    path('create/', document_create, name='document_create'),
    path(
        'required-document/<int:pk>/status/',
        required_document_status_update,
        name='required_document_status_update'
    ),
    path(
        'required-document/<int:pk>/generate-charter/',
        generate_charter,
        name='generate_charter'
    ),
    path('document/<int:pk>/replace/', document_replace, name='document_replace'),
    path('staff/case/<int:pk>/', staff_client_case_detail, name='staff_client_case_detail'),
    path('feedback/', feedback_create, name='feedback_create'),
]