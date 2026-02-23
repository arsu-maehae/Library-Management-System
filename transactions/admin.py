from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # เพิ่ม calculate_fine มาโชว์ในตารางด้วย
    list_display = ('book_copy', 'user', 'borrowed_at', 'due_date', 'status', 'calculate_fine')
    list_filter = ('status',)
    search_fields = ('user__username', 'book_copy__copy_id')