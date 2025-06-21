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
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('users/<int:user_id>/change_role/', views.change_user_role, name='change_user_role'),
    path('appointment/', views.appointment_create, name='appointment_create'),
    path('appointment/success/', views.appointment_success, name='appointment_success'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('admin-panel/', views.custom_admin_panel, name='custom_admin_panel'),
    path('admin-panel/appointments/', views.all_appointments, name='all_appointments'),
    path('admin-panel/departments/', views.admin_departments_list, name='admin_departments_list'),
    path('admin-panel/departments/add/', views.admin_department_edit, name='admin_department_add'),
    path('admin-panel/departments/<int:pk>/edit/', views.admin_department_edit, name='admin_department_edit'),
    path('admin-panel/departments/<int:pk>/delete/', views.admin_department_delete, name='admin_department_delete'),
    path('departments/', views.departments_list, name='departments_list'),
    path('appointments/<int:appointment_id>/edit/', views.edit_appointment, name='admin_edit_appointment'),
    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
