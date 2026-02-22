"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.custom_login, name='login'), # หน้าแรก (http://127.0.0.1:8000/) คือ Login
    path('register/', user_views.register_student, name='register'), # หน้าสมัครสมาชิก
    path('logout/', user_views.custom_logout, name='logout'),
    path('books/', include('books.urls')), # ย้ายหน้าค้นหาหนังสือมาที่นี่
]