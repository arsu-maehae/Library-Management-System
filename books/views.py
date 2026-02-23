from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book, BookCopy
from transactions.models import Transaction # ดึง Transaction จากแอปใหม่
from django.utils import timezone
from datetime import timedelta

def book_list(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'query': query})

@login_required
def borrow_book(request, book_id):
    # 1. หาหนังสือที่ต้องการ
    book = get_object_or_404(Book, id=book_id)
    
    # 2. ถ้านักศึกษากดปุ่ม "ยืนยันการยืม" (ส่งข้อมูลแบบ POST กลับมา)
    if request.method == 'POST':
        # รับค่าจำนวนวันจากหน้าเว็บ (ถ้าไม่เลือกมา ให้ค่าเริ่มต้นคือ 7 วัน)
        days = int(request.POST.get('days', 7))
        
        # ค้นหาเล่มที่ว่างอีกรอบเผื่อมีคนตัดหน้า
        available_copy = book.copies.filter(status='available').first()
        
        if available_copy:
            due_date = timezone.now() + timedelta(days=days)
            Transaction.objects.create(
                user=request.user,
                book_copy=available_copy,
                due_date=due_date
            )
            messages.success(request, f'ยืมหนังสือ "{book.title}" สำเร็จ! (กำหนดคืนในอีก {days} วัน)')
            return redirect('book_list') # 👈 ถ้าคุณใช้วิธีที่ 2 อย่าลืมใส่ books: ด้วยนะครับ
        else:
            messages.error(request, 'ขออภัย หนังสือเพิ่งถูกยืมไปเมื่อสักครู่')
            return redirect('book_list')

    # 3. ถ้าเพิ่งคลิกเข้ามา (แบบ GET) ให้พาไปหน้า "ยืนยันการยืม" ก่อน
    available_copy = book.copies.filter(status='available').first()
    if not available_copy:
        messages.error(request, 'ขออภัย หนังสือเล่มนี้ถูกยืมไปหมดแล้ว')
        return redirect('book_list')

    # ส่งข้อมูลหนังสือและตัวเล่มไปให้หน้า HTML แสดงผล
    return render(request, 'books/borrow_confirm.html', {
        'book': book,
        'copy': available_copy
    })