from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    pin = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        # hash pin field before saving 
        self.pin = make_password(str(self.pin))
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
