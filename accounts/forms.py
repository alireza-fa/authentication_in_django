import random
from datetime import datetime
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import User, OtpCode
from django.contrib.auth import authenticate, login
from .validators import check_phone_number
from django.contrib import messages
from django.core.validators import validate_email
from convert_numbers import persian_to_english


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='confirm password')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href="../password/">this link</a>')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'last_login')


class UserLoginUsernameForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('username')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": _('password')}))

    def __init__(self, request=None, *args, **kwargs):
        super(UserLoginUsernameForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 32:
            raise forms.ValidationError(_('username must less than 32 chars.'))
        return username

    def clean(self):
        cd = self.cleaned_data
        if cd.get('username') and cd.get('password'):
            user = authenticate(username=cd.get('username'), password=cd.get('password'))
            if not user:
                raise forms.ValidationError(_('not found any account with information'))
            login(self.request, user)
        return cd


class UserRegisterUsernameForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('username')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": _('password')}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 32:
            raise forms.ValidationError(_('username must less than 32 chars.'))
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('this username already exist.'))
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError(_('password must have more than or equal 8 chars.'))
        return password


class UserLoginPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _('Phone number')}), validators=[check_phone_number]
    )

    def clean_phone_number(self):
        phone = persian_to_english(self.cleaned_data.get('phone_number'))
        user = User.objects.filter(phone_number=phone).exists()
        if not user:
            raise forms.ValidationError(_('This phone number does not exist.'))
        return phone


class UserRegisterPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _('Phone number')}), validators=[check_phone_number]
    )

    def clean_phone_number(self):
        phone_number = persian_to_english(self.cleaned_data.get('phone_number'))
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise forms.ValidationError(_('This phone number already exist.'))
        return phone_number


class UserLoginEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": _('email')}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if not user:
            raise forms.ValidationError(_('This email does not exist'))
        return email


class UserRegisterEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": _('email')}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError(_('This email already exist.'))
        return email


class VerifyOtpCodeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('code')}))

    def __init__(self, request=None, *args, **kwargs):
        super(VerifyOtpCodeForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(code) < 4 or len(code) > 4:
            raise forms.ValidationError(_('invalid code.'))
        otp_code = OtpCode.objects.filter(code=code)
        if not otp_code.exists():
            raise forms.ValidationError(_('invalid code.'))
        otp_code = otp_code.last()
        if otp_code.expire_time < datetime.now():
            raise forms.ValidationError(_('Expiration time is over'))
        else:
            if otp_code.phone_number:
                user = User.objects.filter(phone_number=otp_code.phone_number)
                if user.exists():
                    login(self.request, user[0], backend='accounts.authenticate.PhoneNumberAuthBackend')
                    messages.success(self.request, _('You have successfully logged in via your mobile number.'))
                else:
                    user = User.objects.create_user(phone_number=otp_code.phone_number)
                    login(self.request, user, backend='accounts.authenticate.PhoneNumberAuthBackend')
                    messages.success(self.request, _('You have successfully registered via your mobile number.'))
            if otp_code.email:
                user = User.objects.filter(email=otp_code.email)
                if user.exists():
                    login(self.request, user[0], backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(self.request, _('You have successfully logged in via your email.'))
                else:
                    user = User.objects.create_user(email=otp_code.email)
                    login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(self.request, _('You have successfully registered via your email'))
            otp_code.delete()
        return code


class UserLoginCombineForm(forms.Form):
    info = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('Email or Phone number')}))

    def clean_info(self):
        info = self.cleaned_data.get('info')
        if '@' in info:
            try:
                validate_email(info)
            except:
                return validate_email(info)
            user = User.objects.filter(email=info).exists()
            if not user:
                raise forms.ValidationError(_('not found any account with information'))
        else:
            info = persian_to_english(info)
            if info:
                check_phone_number(info)
            user = User.objects.filter(phone_number=info).exists()
            if not user:
                raise forms.ValidationError(_('not found any account with information'))
        return info


class UserRegisterCombineForm(forms.Form):
    info = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('Email or Phone number')}))

    def clean_info(self):
        info = self.cleaned_data.get('info')
        if '@' in info:
            try:
                validate_email(info)
            except:
                return validate_email(info)
            user = User.objects.filter(email=info).exists()
            if user:
                raise forms.ValidationError(_('This email already exist.'))
        else:
            info = persian_to_english(info)
            if info:
                check_phone_number(info)
            user = User.objects.filter(phone_number=info).exists()
            if user:
                raise forms.ValidationError(_('This phone number already exist.'))
        return info
