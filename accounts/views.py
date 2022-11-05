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
from django.conf import settings
import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_API_PRIVATE_KEY


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
        # creating stripe 
        if not profile.stripe_id:# check if stripe id exist
            stripeProfile = stripe.Customer.create()# create a stripe profile
            profile.stripe_id = stripeProfile['id']# assign stripe id from stripeProfile to stripe_id of profile
            profile.save()# save the profile in database
        # get stripe payment method
        stripe_payment_method = stripe.PaymentMethod.list(
            customer = profile.stripe_id,
            type="card"
        )
        print(stripe_payment_method)
        if stripe_payment_method and len(stripe_payment_method.data)>0:
            payment_method = stripe_payment_method.data[0]
            profile.stripe_payment_method_id = payment_method.id
            profile.stripe_card_last4 = payment_method.card.last4
            profile.save()
        else:
            profile.stripe_payment_method_id =""
            profile.stripe_card_last4 =""
            profile.save()
        intent = stripe.SetupIntent.create(
            customer = profile.stripe_id
        )
        context = {
            'profile':profile,
            'profile_form':profile_form,
            'user_form':user_form,
            'password_change_form':password_change_form,
            'client_secret': intent.client_secret,
            'STRIPE_API_PUBLIC_KEY':settings.STRIPE_API_PUBLIC_KEY,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.user_profile)
        password_change_form = UserPasswordChangeForm(request.user, request.POST)
        if 'profile_update' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Info Updated')
                return redirect('accounts:profile')
            else:
                password_change_form = UserPasswordChangeForm(request.user)
                user_form = CustomUserChangeForm(request.POST, instance=request.user)
                profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.user_profile)
        elif 'change_password' in request.POST:
            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password change Successfull')
                return redirect('accounts:profile') 
            else:
                
                user_form = CustomUserChangeForm(instance=request.user)
                profile_form = ProfileForm(instance=request.user.user_profile)           
        context = {
            'profile':profile,
            'user_form':user_form,
            'profile_form':profile_form,
            'password_change_form':password_change_form,
        }
        return render(request, self.template_name, context)