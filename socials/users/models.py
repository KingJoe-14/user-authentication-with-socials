from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, middle_name, last_name, phone, password=None):
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
        )
        user.set_password(password)  # ✅ hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, middle_name, last_name, phone, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name', 'phone']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
