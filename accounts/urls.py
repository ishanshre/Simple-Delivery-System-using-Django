from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.UserSignUp.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile')
]