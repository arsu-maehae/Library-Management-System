from django.contrib import admin

# Register your models here.

from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_at', 'due_date', 'status')
    list_filter = ('status', 'borrowed_at')
    search_fields = ('book__title', 'user__username')