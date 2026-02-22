from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

# เพิ่มช่อง 'role' เข้าไปในหน้าจอ Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    # เพิ่ม field role ลงในหน้าแก้ไขข้อมูล
    fieldsets = UserAdmin.fieldsets + (
        ('Library Role', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)