from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name') # ให้กรอกแค่นี้พอ

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'member'  # 🔒 ล็อกสิทธิ์! สมัครเองเป็นได้แค่นักศึกษา
        if commit:
            user.save()
        return user