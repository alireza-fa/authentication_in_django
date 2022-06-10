from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView


app_name = 'accounts'

login = [
    path('username/', views.UserLoginUsernameView.as_view(), name='login_username'),
    path('phone_number/', views.UserLoginPhoneNumberView.as_view(), name='login_phone_number'),
    path('email/', views.UserLoginEmailView.as_view(), name='login_email'),
    path('combine/', views.UserLoginCombineView.as_view(), name='login_combine'),
]

register = [
    path('username/', views.UserRegisterUsernameView.as_view(), name='register_username'),
    path('phone_number/', views.UserRegisterPhoneNumberView.as_view(), name='register_phone_number'),
    path('email/', views.UserRegisterEmailView.as_view(), name='register_email'),
    path('combine/', views.UserRegisterCombineView.as_view(), name='register_combine'),
]

urlpatterns = [
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('login/', include(login)),
    path('register/', include(register)),
    path('verify_otp_code/', views.VerifyOtpCodeView.as_view(), name='verify_otp'),
    path('login_and_register/github/', TemplateView.as_view(template_name='accounts/github.html'), name='login_register_github'),
    path('login_and_register/google/', TemplateView.as_view(template_name='accounts/google.html'), name='login_register_google'),
    path('api/', include('accounts.api_urls')),
]
