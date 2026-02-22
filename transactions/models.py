from django.db import models

# Create your models here.

from django.conf import settings
from books.models import Book
from django.utils import timezone # เพิ่มตัวจัดการเวลา

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('borrowed', 'กำลังยืม'),
            ('returned', 'คืนแล้ว'),
            ('overdue', 'เกินกำหนด'),
        ],
        default='borrowed'
    )

    def __str__(self):
        return f"{self.user.username} ยืม {self.book.title}"

    # --- เพิ่ม Logic อัจฉริยะตรงนี้ ---
    def save(self, *args, **kwargs):
        # 1. ถ้าเป็นการยืมหนังสือใหม่
        if self.pk is None and self.status == 'borrowed':
            self.book.status = 'borrowed' # เปลี่ยนสถานะหนังสือเป็น 'ถูกยืม'
            self.book.save()              # เซฟหนังสือ
        
        # 2. ถ้ามีการกดเปลี่ยนสถานะเป็น 'คืนแล้ว'
        elif self.pk is not None and self.status == 'returned' and not self.returned_at:
            self.book.status = 'available' # คืนหนังสือกลับชั้น (ว่าง)
            self.book.save()               # เซฟหนังสือ
            self.returned_at = timezone.now() # ประทับเวลาคืนหนังสืออัตโนมัติ

        super().save(*args, **kwargs) # สั่งให้บันทึก Transaction ตามปกติ

    @property
    def calculate_fine(self):
        """
        คำนวณค่าปรับอัตโนมัติ (สมมติวันละ 10 บาท)
        """
        fine_per_day = 10
        
        # 1. กรณีที่ยังไม่คืน (กำลังยืม หรือ เกินกำหนด)
        if self.status in ['borrowed', 'overdue']:
            # ถ้าเวลาปัจจุบัน มากกว่า วันที่กำหนดคืน
            if timezone.now() > self.due_date:
                # คำนวณส่วนต่างเป็นจำนวนวัน
                days_late = (timezone.now() - self.due_date).days
                return days_late * fine_per_day
                
        # 2. กรณีที่คืนแล้ว ให้คิดค่าปรับจากวันที่นำมาคืน
        elif self.status == 'returned' and self.returned_at:
            if self.returned_at > self.due_date:
                days_late = (self.returned_at - self.due_date).days
                return days_late * fine_per_day
                
        # ถ้ายังไม่ถึงกำหนด หรือคืนตรงเวลา ค่าปรับ = 0
        return 0