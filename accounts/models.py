from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True, verbose_name=_('username'))
    email = models.EmailField(max_length=120, unique=True, null=True, blank=True, verbose_name=_('email'))
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name=_('phone number'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number', )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin


class EffortAuthenticate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='efforts', verbose_name=_('user'))
    count = models.PositiveSmallIntegerField(verbose_name=_('count'))
    lock_time = models.DateTimeField(verbose_name=_('lock time'))

    class Meta:
        verbose_name = _('Effort Authenticate')
        verbose_name_plural = _('Efforts authenticate')

    def __str__(self):
        return self.user


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name=_('phone number'))
    email = models.CharField(max_length=11, null=True, blank=True, verbose_name=_('email'))
    code = models.CharField(max_length=4, verbose_name=_('code'))
    expire_time = models.DateTimeField(verbose_name=_('expire time'))

    class Meta:
        verbose_name = _('Otp code')
        verbose_name_plural = _('Otp codes')

    def __str__(self):
        return self.code
