from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from .models import Profile
class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta(UserCreationForm.Meta):
        
        model = get_user_model()
        fields = ['first_name','last_name','age','gender','username','email','captcha']


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','age','gender','username','email']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username','password','remember_me']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio','country','address','phoneNumber']
