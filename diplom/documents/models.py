from django.db import models
from django.contrib.auth.models import User


class DocumentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    required_documents = models.ManyToManyField(
        DocumentType,
        blank=True,
        related_name='services'
    )

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)

    def __str__(self):
        return self.full_name


class ClientCase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)

    organization_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Название организации'
    )

    short_organization_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Сокращённое название организации'
    )

    legal_address = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Юридический адрес'
    )

    director_full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ФИО руководителя'
    )

    authorized_capital = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Уставный капитал'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client} — {self.service_type}"


class RequiredDocument(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидается'),
        ('uploaded', 'Загружен'),
        ('brought_personally', 'Принесён лично'),
        ('not_required', 'Не требуется'),
        ('verified', 'Проверен'),
        ('rejected', 'Отклонен'),
    ]

    client_case = models.ForeignKey(
        ClientCase,
        on_delete=models.CASCADE,
        related_name='required_documents'
    )
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='waiting')
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.document_type} — {self.get_status_display()}"


class Document(models.Model):
    required_document = models.ForeignKey(
        RequiredDocument,
        on_delete=models.CASCADE,
        related_name='files'
    )

    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True, null=True)
    extracted_full_name = models.CharField(max_length=255, blank=True, null=True)
    extracted_inn = models.CharField(max_length=12, blank=True, null=True)
    extracted_document_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.required_document.document_type} — {self.required_document.client_case.client}"
    
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ClientCase)
def create_required_documents(sender, instance, created, **kwargs):
    if created:
        service = instance.service_type
        document_types = service.required_documents.all()

        for doc_type in document_types:
            RequiredDocument.objects.create(
                client_case=instance,
                document_type=doc_type
            )


class Feedback(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыта'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Тема'
    )

    message = models.TextField(
        verbose_name='Описание проблемы'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"{self.title} — {self.get_status_display()}"