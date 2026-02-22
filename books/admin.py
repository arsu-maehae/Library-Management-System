from django.contrib import admin

# Register your models here.

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # กำหนดให้หน้า Admin แสดงคอลัมน์อะไรบ้าง
    list_display = ('title', 'author', 'isbn', 'status', 'updated_at')
    # เพิ่มช่องค้นหา
    search_fields = ('title', 'author', 'isbn')
    # เพิ่มตัวกรองด้านขวามือ
    list_filter = ('status',)
