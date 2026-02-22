from django.contrib import admin

# Register your models here.

from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # เพิ่ม 'calculate_fine' เข้ามาใน list_display
    list_display = ('book', 'user', 'borrowed_at', 'due_date', 'status', 'calculate_fine')
    list_filter = ('status', 'borrowed_at')
    search_fields = ('book__title', 'user__username')