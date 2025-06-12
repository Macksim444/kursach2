from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import CustomUser

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

