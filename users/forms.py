from django import forms
from .models import User

class StudentSignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}) # สามารถใส่ class ให้สวยขึ้นได้
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name') 
        
        # ✨ เพิ่มบล็อกนี้เข้าไปเพื่อลบข้อความ Default ของ Django ✨
        help_texts = {
            'username': '', 
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'member'
        if commit:
            user.save()
        return user