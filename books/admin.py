from django.contrib import admin
from .models import Book, BookCopy

class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 3

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    inlines = [BookCopyInline]

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('copy_id', 'book', 'status')
    list_filter = ('status', 'book')
    search_fields = ('copy_id', 'book__title')