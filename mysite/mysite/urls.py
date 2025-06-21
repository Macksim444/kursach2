from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', include('visitors.urls')),
    path('', include('visitors.urls')),  # главная страница и остальные маршруты без префикса
]
