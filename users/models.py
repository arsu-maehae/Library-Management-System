from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # กำหนด Role ให้ระบบ
    ROLE_CHOICES = (
        ('member', 'Member (นักศึกษา)'),
        ('librarian', 'Librarian (บรรณารักษ์)'),
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='member',
        verbose_name="ตำแหน่ง"
    )

    def is_librarian(self):
        return self.role == 'librarian'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"