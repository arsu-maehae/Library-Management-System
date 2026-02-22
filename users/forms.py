from django import forms
from .models import User

# เปลี่ยนจากการสืบทอด UserCreationForm มาใช้ ModelForm ธรรมดา
class StudentSignUpForm(forms.ModelForm):
    # สร้างช่องกรอกรหัสผ่านแบบง่ายๆ ไม่ต้องมีกฎเกณฑ์
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name') # ช่องที่บังคับให้กรอก

    def save(self, commit=True):
        # 1. จำลองการเซฟข้อมูลมาไว้ในตัวแปร user ก่อน
        user = super().save(commit=False)
        
        # 2. เอารหัสผ่านที่พิมพ์มาเข้ารหัส (Hash) ให้ระบบอ่านเข้าใจ
        user.set_password(self.cleaned_data['password'])
        
        # 3. ล็อกสิทธิ์เป็นนักศึกษา (Member) เหมือนเดิม
        user.role = 'member'
        
        # 4. บันทึกลง Database ของจริง
        if commit:
            user.save()
        return user