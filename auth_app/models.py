from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsersManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        if not login:
            raise ValueError("Логин обязателен")

        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    fullName = models.CharField(max_length=50)
    login = models.CharField(max_length=20, unique=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsersManager()
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.login