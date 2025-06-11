from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

User = get_user_model()

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
    if filter_status == 'blocked':
        users = User.objects.filter(is_blocked=True)
    elif filter_status == 'active':
        users = User.objects.filter(is_blocked=False)
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

