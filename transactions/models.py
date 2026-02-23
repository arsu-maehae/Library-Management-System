from django.db import models
from django.conf import settings
from books.models import BookCopy # 👈 เปลี่ยนมาดึง BookCopy แทน Book
from django.utils import timezone

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', verbose_name="ผู้ยืม")
    
    # 👈 จุดสำคัญ: ชี้ไปที่ BookCopy (บาร์โค้ด) ไม่ใช่ Book (หน้าปก)
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='transactions', verbose_name="เล่มที่ยืม (บาร์โค้ด)")
    
    borrowed_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ยืม")
    due_date = models.DateTimeField(verbose_name="กำหนดคืน")
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name="วันที่คืนจริง")
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('borrowed', 'กำลังยืม'),
            ('returned', 'คืนแล้ว'),
            ('overdue', 'เกินกำหนด'),
        ],
        default='borrowed',
        verbose_name="สถานะการยืม"
    )

    def __str__(self):
        return f"{self.user.username} ยืม {self.book_copy.copy_id}"

    # --- Logic อัจฉริยะ (อัปเกรดให้รองรับ BookCopy) ---
    def save(self, *args, **kwargs):
        # 1. ถ้าเป็นการยืมหนังสือใหม่
        if self.pk is None and self.status == 'borrowed':
            self.book_copy.status = 'borrowed' # 👈 เปลี่ยนสถานะของ "ตัวเล่ม(บาร์โค้ด)"
            self.book_copy.save()
        
        # 2. ถ้ามีการกดเปลี่ยนสถานะเป็น 'คืนแล้ว'
        elif self.pk is not None and self.status == 'returned' and not self.returned_at:
            self.book_copy.status = 'available' # 👈 คืน "ตัวเล่ม(บาร์โค้ด)" กลับชั้น
            self.book_copy.save()
            self.returned_at = timezone.now()

        super().save(*args, **kwargs)

    @property
    def calculate_fine(self):
        fine_per_day = 10
        if self.status in ['borrowed', 'overdue']:
            if timezone.now() > self.due_date:
                days_late = (timezone.now() - self.due_date).days
                return days_late * fine_per_day
        elif self.status == 'returned' and self.returned_at:
            if self.returned_at > self.due_date:
                days_late = (self.returned_at - self.due_date).days
                return days_late * fine_per_day
        return 0