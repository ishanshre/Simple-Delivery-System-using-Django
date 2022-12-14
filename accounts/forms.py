from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
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
    profile_update = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Profile
        fields = ['avatar','bio','country','address','phoneNumber']
        widgets = {
            'phoneNumber': PhoneNumberPrefixWidget(initial="NP")
        }

class UserPasswordChangeForm(PasswordChangeForm):
    change_password = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']
    