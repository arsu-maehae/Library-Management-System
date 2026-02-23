from django.db import models

# 1. ตารางข้อมูลหน้าปกหนังสือ (Book) - เก็บแค่ข้อมูลทั่วไป
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="ชื่อหนังสือ")
    author = models.CharField(max_length=200, verbose_name="ผู้แต่ง")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="รหัส ISBN")

    def __str__(self):
        return self.title
    
    @property
    def available_count(self):
        # ให้นับจำนวน BookCopy ของหนังสือเล่มนี้ ที่มีสถานะเป็น 'available'
        return self.copies.filter(status='available').count()

# 2. ตารางตัวเล่มจริง (BookCopy) - เก็บข้อมูลบาร์โค้ดและสถานะ
class BookCopy(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available (พร้อมให้ยืม)'),
        ('borrowed', 'Borrowed (ถูกยืม)'),
        ('lost', 'Lost/Damaged (ชำรุด/สูญหาย)'),
        ('maintenance', 'Maintenance (ซ่อมบำรุง)'),
    )
    
    copy_id = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name="รหัสบาร์โค้ด (Copy ID)")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies', verbose_name="ชื่อหนังสือ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="สถานะ")

    def __str__(self):
        return f"{self.book.title} [รหัส: {self.copy_id}]"