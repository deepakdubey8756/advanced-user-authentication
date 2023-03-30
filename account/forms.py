from .models import Profile
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput)
    confirmPass = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput)