from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Appointment
from .models import Department
from .forms import DepartmentForm
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods

@staff_member_required
def admin_departments_list(request):
    departments = Department.objects.all()
    return render(request, 'visitors/admin_departments_list.html', {'departments': departments})

@require_http_methods(["GET", "POST"])
def admin_department_edit(request, pk=None):
    if pk:
        department = get_object_or_404(Department, pk=pk)
    else:
        department = None

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отдел успешно сохранён.')
            return redirect(reverse('admin_departments_list'))
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'visitors/admin_department_form.html', {'form': form, 'department': department})

@require_http_methods(["POST"])
def admin_department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Отдел удалён.')
    return redirect(reverse('admin_departments_list'))

def departments_list(request):
    departments = Department.objects.all()
    return render(request, 'visitors/departments_list.html', {'departments': departments})

@staff_member_required
def all_appointments(request):
    appointments = Appointment.objects.select_related('user').all().order_by('-created_at')
    return render(request, 'visitors/all_appointments.html', {'appointments': appointments})

@staff_member_required
def custom_admin_panel(request):
    return render(request, 'visitors/custom_admin_panel.html')

@login_required
def my_appointments(request):
    appointments = request.user.appointments.all()
    return render(request, 'visitors/my_appointments.html', {'appointments': appointments})

def appointment_success(request):
    return render(request, 'visitors/appointment_success.html')

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # связываем с текущим пользователем
            try:
                appointment.save()
                messages.success(request, 'Ваша запись успешно создана.')
                return redirect('appointment_success')  # или на другую страницу
            except IntegrityError:
                form.add_error(None, 'Ошибка: запись с такими данными уже существует.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AppointmentForm()
    return render(request, 'visitors/appointment_form.html', {'form': form})
User = get_user_model()

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def change_user_role(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        new_role = request.POST.get('role')
        if new_role in ['visitor', 'staff']:
            user.role = new_role
            user.save()
            messages.success(request, f'Роль пользователя {user.username} обновлена.')
        else:
            messages.error(request, 'Неверная роль.')
    return redirect('users_list')  # замените на имя вашего url списка пользователей

@staff_member_required  # доступ только для администраторов
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:  # чтобы админ не мог заблокировать себя
        user.is_blocked = True
        user.save()
    return redirect(reverse('users_list'))

@staff_member_required
def users_list(request):
    filter_status = request.GET.get('status', 'all')
    if filter_status == 'admins':
        users = User.objects.filter(is_superuser=True)
    elif filter_status == 'staff':
        users = User.objects.filter(role='staff', is_superuser=False)
    elif filter_status == 'visitor':
        users = User.objects.filter(role='visitor', is_superuser=False)
    else:
        users = User.objects.all()
    return render(request, 'visitors/users_list.html', {'users': users, 'filter_status': filter_status})

@staff_member_required
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.is_blocked = False
        user.save()
    return redirect(reverse('users_list'))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'visitors/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'visitors/login.html', {'form': form})

def home(request):
    return render(request, 'visitors/home.html')

def about(request):
    return render(request, 'visitors/about.html')

