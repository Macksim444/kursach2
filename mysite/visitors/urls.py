from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('users/', views.users_list, name='users_list'),
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
path('users/<int:user_id>/change_role/', views.change_user_role, name='change_user_role'),
]
