from django.shortcuts import render
from .forms import CustomUserCreationForm, UserLoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
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