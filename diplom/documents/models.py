from django.db import models

class Document(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('review', 'На рассмотрении'),
        ('approved', 'Подтвержден'),
        ('rejected', 'Отклонен'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title