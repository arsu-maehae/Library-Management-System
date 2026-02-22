from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # เมื่อเข้ามาที่หน้าหลักของแอป books ให้เรียกใช้ฟังก์ชัน book_list
    path('', views.book_list, name='book_list'),
]