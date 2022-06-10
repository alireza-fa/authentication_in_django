from django.contrib.auth.models import BaseUserManager
import random


class UserManager(BaseUserManager):

    def create_user(self, password=None, phone_number=None, email=None, username=None):
        if not username:
            username = str(random.randint(10000000000, 9999999999999999))
        if not password:
            password = str(random.randint(10000000, 99999999))
        user = self.model(username=username, phone_number=phone_number)
        if email:
            email = BaseUserManager.normalize_email(email)
            user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, phone_number, username=None):
        if not email:
            raise ValueError('superuser must have email address.')
        if not phone_number:
            raise ValueError('superuser must have phone number.')
        user = self.create_user(password=password, email=email, phone_number=phone_number, username=username)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
