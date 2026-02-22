
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentSignUpForm
from django.views.decorators.cache import never_cache # 👈 เพิ่มบรรทัดนี้

@never_cache # 🔒 เพิ่มตัวนี้เพื่อป้องกันการแคชหน้า login
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # 🔀 ตรวจสอบ Role เพื่อแยกทางไป
            if user.role == 'librarian' or user.is_superuser:
                return redirect('/admin/') # บรรณารักษ์ไปหน้าหลังบ้าน
            else:
                return redirect('/books/') # นักศึกษาไปหน้าค้นหาหนังสือ
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # สมัครเสร็จให้ Login อัตโนมัติเลย
            return redirect('/books/')
    else:
        form = StudentSignUpForm()
    return render(request, 'users/register.html', {'form': form})

def custom_logout(request):
    logout(request) # สั่งทำลายตั๋ว (Session)
    return redirect('/') # เตะกลับไปหน้า Login