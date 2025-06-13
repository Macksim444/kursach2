from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField('Название отдела', max_length=200)
    description = models.TextField('Описание отдела')
    employees = models.TextField('Сотрудники отдела (через запятую)')
    working_hours = models.CharField('Время работы отдела', max_length=100)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name

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

class Appointment(models.Model):
    VISIT_PURPOSE_CHOICES = [
        ('credit', 'Кредит'),
        ('mortgage', 'Ипотека'),
        ('consultation', 'Консультация'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Пользователь',
        null=True,
        blank=True,
        help_text='Пользователь, который записался на встречу (если авторизован)'
    )
    last_name = models.CharField('Фамилия', max_length=150)
    first_name = models.CharField('Имя', max_length=150)
    middle_name = models.CharField('Отчество', max_length=150, blank=True)
    phone = models.CharField('Номер телефона', max_length=20)
    visit_purpose = models.CharField('Цель визита', max_length=20, choices=VISIT_PURPOSE_CHOICES)

    created_at = models.DateTimeField('Дата создания записи', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись на встречу'
        verbose_name_plural = 'Записи на встречу'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.last_name} {self.first_name} — {self.get_visit_purpose_display()}'