from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Department

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(required=False, label='Телефон')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    patronymic = forms.CharField(required=False, label='Отчество')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'patronymic', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['last_name', 'first_name', 'middle_name', 'phone', 'visit_purpose']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'phone': 'Номер телефона',
            'visit_purpose': 'Цель визита',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию',
                'autocomplete': 'family-name',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'autocomplete': 'given-name',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество',
                'autocomplete': 'additional-name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__',
                'type': 'tel',
                'pattern': r'^\+?\d{7,15}$',
                'title': 'Введите корректный номер телефона',
                'autocomplete': 'tel',
            }),
            'visit_purpose': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'employees', 'working_hours']
        widgets = {
            'working_hours': forms.TextInput(attrs={'placeholder': 'Например, Пн-Пт 9:00-18:00'}),
            'employees': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Иванов И., Петров П., ...'}),
        }