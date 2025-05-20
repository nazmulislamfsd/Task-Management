from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None


class CustomRegForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("password must be at least 8 character long")
        
        elif not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
            raise forms.ValidationError("password must be Upper-case, Lower-case, Number and Special Character(@#$%^&+=) only")
        
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and  password1 != confirm_password:
            raise forms.ValidationError("password don't match!")
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email=email).exists()

        if email_exist:
            raise forms.ValidationError("this email already exist!")
        
        return email