from django.shortcuts import render

# Create your views here.

from django.db.models import Q
from .models import Book

def book_list(request):
    # ดึงคำค้นหาที่ user พิมพ์มา (ถ้ามี)
    query = request.GET.get('q', '')
    
    if query:
        # ค้นหาทั้งจาก ชื่อหนังสือ (title) และ ชื่อผู้แต่ง (author)
        # icontains คือการหาคำที่ตรงกันบางส่วน (ไม่สนพิมพ์เล็ก-ใหญ่)
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        # ถ้าไม่ได้พิมพ์อะไรมาเลย ให้แสดงหนังสือทั้งหมด
        books = Book.objects.all()
        
    return render(request, 'books/book_list.html', {'books': books, 'query': query})