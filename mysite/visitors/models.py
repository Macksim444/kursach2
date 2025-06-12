from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('visitor', 'Посетитель'),
        ('staff', 'Сотрудник'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='visitor')

    @property
    def is_staff_member(self):
        return self.role == 'staff' or self.is_superuser

    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    is_blocked = models.BooleanField('Заблокирован', default=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
