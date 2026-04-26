from django.contrib import admin
from .models import (
    DocumentType,
    ServiceType,
    Client,
    ClientCase,
    RequiredDocument,
    Document,
    Feedback,
)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    filter_horizontal = ('required_documents',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'inn', 'user')
    search_fields = ('full_name', 'inn', 'user__username')


class RequiredDocumentInline(admin.TabularInline):
    model = RequiredDocument
    extra = 0


@admin.register(ClientCase)
class ClientCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'service_type', 'created_at', 'is_complete')
    list_filter = ('service_type', 'is_complete')
    search_fields = ('client__full_name', 'client__inn')
    inlines = [RequiredDocumentInline]


@admin.register(RequiredDocument)
class RequiredDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_case', 'document_type', 'status')
    list_filter = ('status', 'document_type')
    search_fields = (
        'client_case__client__full_name',
        'client_case__client__inn',
        'document_type__name',
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'required_document', 'uploaded_at')
    search_fields = (
        'required_document__client_case__client__full_name',
        'required_document__client_case__client__inn',
        'required_document__document_type__name',
        'extracted_text',
        'extracted_full_name',
        'extracted_inn',
        'extracted_document_number',
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'message', 'user__username')