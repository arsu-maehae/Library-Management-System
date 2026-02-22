# Create your views here.

from django.shortcuts import render
from django.db.models import Q
from .models import Book
from django.contrib.auth.decorators import login_required # นำเข้าตัวล็อก

# 🔒 ใส่ @login_required ไว้บนฟังก์ชัน ถ้าไม่ login จะเด้งไปหน้า '/' (หน้า login)
@login_required(login_url='/') 
def book_list(request):
    # ... (โค้ดดึงข้อมูลหนังสือของคุณเหมือนเดิมทุกอย่างเลยครับ) ...
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'query': query})