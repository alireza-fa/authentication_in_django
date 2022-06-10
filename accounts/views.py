from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import logout
from .forms import UserLoginUsernameForm, UserRegisterUsernameForm, UserLoginPhoneNumberForm, UserRegisterPhoneNumberForm, \
    VerifyOtpCodeForm, UserLoginEmailForm, UserRegisterEmailForm, UserLoginCombineForm, UserRegisterCombineForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import User, OtpCode
import random
from .tasks import send_sms_code_task, send_mail_code_task
from datetime import datetime, timedelta


class BaseView(View):
    template_name = None
    class_form = None
    form_need_request = False

    def get(self, request):
        return render(request, self.template_name, {"form": self.class_form()})

    def post(self, request):
        if self.form_need_request:
            form = self.class_form(request=request, data=request.POST)
        else:
            form = self.class_form(data=request.POST)
        if form.is_valid():
            return self.is_valid(request, form)
        return render(request, self.template_name, {"form": form})

    def is_valid(self, request, form):
        pass


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:home')


class UserLoginUsernameView(BaseView):
    template_name = 'accounts/login_username.html'
    class_form = UserLoginUsernameForm
    form_need_request = True

    def is_valid(self, request, form):
        messages.success(request, _('you are logged in with username and password successfully.'))
        return redirect('core:home')


class UserRegisterUsernameView(BaseView):
    template_name = 'accounts/register_username.html'
    class_form = UserRegisterUsernameForm

    def is_valid(self, request, form):
        cd = form.cleaned_data
        User.objects.create_user(username=cd.get('username'), password=cd.get('password'))
        messages.success(request, _('You have successfully registered with your username and password.'))
        return redirect('core:home')


class UserLoginPhoneNumberView(BaseView):
    template_name = 'accounts/login_phone_number.html'
    class_form = UserLoginPhoneNumberForm

    def is_valid(self, request, form):
        code = str(random.randint(1000, 9999))
        phone = form.cleaned_data.get('phone_number')
        OtpCode.objects.create(phone_number=phone, code=code, expire_time=datetime.now() + timedelta(minutes=2))
        send_sms_code_task.delay(phone, code)
        messages.success(request, _('We have sent a code to your phone number.'))
        return redirect('accounts:verify_otp')


class UserRegisterPhoneNumberView(BaseView):
    template_name = 'accounts/register_phone_number.html'
    class_form = UserRegisterPhoneNumberForm

    def is_valid(self, request, form):
        code = str(random.randint(1000, 9999))
        phone = form.cleaned_data.get('phone_number')
        OtpCode.objects.create(phone_number=phone, code=code, expire_time=datetime.now() + timedelta(minutes=2))
        send_sms_code_task.delay(phone, code)
        messages.success(request, _('We have sent a code to your phone number.'))
        return redirect('accounts:verify_otp')


class VerifyOtpCodeView(BaseView):
    template_name = 'accounts/verify_otp_code.html'
    class_form = VerifyOtpCodeForm
    form_need_request = True

    def is_valid(self, request, form):
        return redirect('core:home')


class UserLoginEmailView(BaseView):
    template_name = 'accounts/login_email.html'
    class_form = UserLoginEmailForm

    def is_valid(self, request, form):
        code = str(random.randint(1000, 9999))
        email = form.cleaned_data.get('email')
        OtpCode.objects.create(email=email, code=code, expire_time=datetime.now() + timedelta(minutes=2))
        send_mail_code_task.delay(email, code)
        messages.success(request, _('We have sent a code to your email.'))
        return redirect('accounts:verify_otp')


class UserRegisterEmailView(BaseView):
    template_name = 'accounts/register_email.html'
    class_form = UserRegisterEmailForm

    def is_valid(self, request, form):
        code = str(random.randint(1000, 9999))
        email = form.cleaned_data.get('email')
        OtpCode.objects.create(email=email, code=code, expire_time=datetime.now() + timedelta(minutes=2))
        send_mail_code_task.delay(email, code)
        messages.success(request, _('We have sent a code to your email.'))
        return redirect('accounts:verify_otp')


class UserLoginCombineView(BaseView):
    template_name = 'accounts/login_combine.html'
    class_form = UserLoginCombineForm

    def is_valid(self, request, form):
        code = str(random.randint(1000, 9999))
        info = form.cleaned_data.get('info')
        expire_time = datetime.now() + timedelta(minutes=2)
        if '@' in info:
            OtpCode.objects.create(email=info, code=code, expire_time=expire_time)
            send_mail_code_task.delay(info, code)
            messages.success(request, _('We have sent a code to your email.'))
        else:
            OtpCode.objects.create(phone_number=info, code=code, expire_time=expire_time)
            send_sms_code_task.delay(info, code)
            messages.success(request, _('We have sent a code to your phone number.'))
        return redirect('accounts:verify_otp')


class UserRegisterCombineView(BaseView):
    template_name = 'accounts/register_combine.html'
    class_form = UserRegisterCombineForm

    def is_valid(self, request, form):
        code = str(random.randint(1000, 9999))
        info = form.cleaned_data.get('info')
        expire_time = datetime.now() + timedelta(minutes=2)
        if '@' in info:
            OtpCode.objects.create(email=info, code=code, expire_time=expire_time)
            send_mail_code_task.delay(info, code)
            messages.success(request, _('We have sent a code to your email.'))
        else:
            OtpCode.objects.create(phone_number=info, code=code, expire_time=expire_time)
            send_sms_code_task.delay(info, code)
            messages.success(request, _('We have sent a code to your phone number.'))
        return redirect('accounts:verify_otp')

