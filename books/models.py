from django.db import models

# Create your models here.

class Book(models.Model):
    # กำหนดสถานะที่เป็นไปได้ของหนังสือ
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
    ]

    title = models.CharField(max_length=255, verbose_name="ชื่อหนังสือ")
    author = models.CharField(max_length=255, verbose_name="ผู้แต่ง")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="รหัส ISBN")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available',
        verbose_name="สถานะ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.isbn})"
