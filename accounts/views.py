from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserLoginForm, ProfileForm, CustomUserChangeForm, UserPasswordChangeForm
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth import update_session_auth_hash # used in changing user password
from django.contrib import messages
# Create your views here.


class UserSignUp(SuccessMessageMixin,CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    message = 'User Created Successfully'
    success_url = reverse_lazy('accounts:login')


    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('delivery:index')
        return super(UserSignUp, self).dispatch(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    message = 'Login Successfull'
    
    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(UserLoginView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('delivery:index')
        return super().dispatch(request, *args, **kwargs)



class UserProfileView(LoginRequiredMixin,View):
    template_name = 'accounts/profile.html'
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.user_profile)
        password_change_form = UserPasswordChangeForm(request.user)
        context = {
            'profile':profile,
            'profile_form':profile_form,
            'user_form':user_form,
            'password_change_form':password_change_form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.user_profile)
        password_change_form = UserPasswordChangeForm(request.user, request.POST)
        if 'change_password' in request.POST:

            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password change Successfull')
                return redirect('accounts:profile')
        if 'profile_update' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Info Updated')
                return redirect('accounts:profile')
        context = {
            'profile':profile,
            'user_form':user_form,
            'profile_form':profile_form,
            'password_change_form':password_change_form,
        }
        return render(request, self.template_name, context)