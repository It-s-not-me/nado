from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DocumentType(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField('Название', max_length=255)
    required_documents = models.ManyToManyField(
        DocumentType,
        blank=True,
        related_name='services',
        verbose_name='Обязательные документы'
    )

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    full_name = models.CharField('ФИО', max_length=255)
    inn = models.CharField('ИНН', max_length=12)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.full_name


class ClientCase(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        verbose_name='Тип услуги'
    )

    organization_name = models.CharField(
        'Название организации',
        max_length=255,
        blank=True,
        null=True
    )

    short_organization_name = models.CharField(
        'Сокращённое название организации',
        max_length=255,
        blank=True,
        null=True
    )

    legal_address = models.CharField(
        'Юридический адрес',
        max_length=500,
        blank=True,
        null=True
    )

    director_full_name = models.CharField(
        'ФИО руководителя',
        max_length=255,
        blank=True,
        null=True
    )

    authorized_capital = models.CharField(
        'Уставный капитал',
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_complete = models.BooleanField('Комплект собран', default=False)

    class Meta:
        verbose_name = 'Дело клиента'
        verbose_name_plural = 'Дела клиентов'

    def __str__(self):
        return f"{self.client} — {self.service_type}"


class RequiredDocument(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидается'),
        ('uploaded', 'Загружен'),
        ('brought_personally', 'Принесён лично'),
        ('not_required', 'Не требуется'),
        ('verified', 'Проверен'),
        ('rejected', 'Отклонён'),
    ]

    client_case = models.ForeignKey(
        ClientCase,
        on_delete=models.CASCADE,
        related_name='required_documents',
        verbose_name='Дело клиента'
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        verbose_name='Тип документа'
    )
    status = models.CharField(
        'Статус',
        max_length=30,
        choices=STATUS_CHOICES,
        default='waiting'
    )
    comment = models.TextField('Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = 'Обязательный документ'
        verbose_name_plural = 'Обязательные документы'

    def __str__(self):
        return f"{self.document_type} — {self.get_status_display()}"


class Document(models.Model):
    required_document = models.ForeignKey(
        RequiredDocument,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Обязательный документ'
    )

    file = models.FileField('Файл', upload_to='documents/')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    extracted_text = models.TextField(
        'Извлечённый текст',
        blank=True,
        null=True
    )
    extracted_full_name = models.CharField(
        'Извлечённое ФИО',
        max_length=255,
        blank=True,
        null=True
    )
    extracted_inn = models.CharField(
        'Извлечённый ИНН',
        max_length=12,
        blank=True,
        null=True
    )
    extracted_document_number = models.CharField(
        'Извлечённый номер документа',
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Загруженный документ'
        verbose_name_plural = 'Загруженные документы'

    def __str__(self):
        return f"{self.required_document.document_type} — {self.required_document.client_case.client}"


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
        'Тема',
        max_length=255
    )

    message = models.TextField(
        'Описание проблемы'
    )

    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f"{self.title} — {self.get_status_display()}"