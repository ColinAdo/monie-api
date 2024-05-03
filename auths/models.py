from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=False)
    phone_number = PhoneNumberField(unique=True)
    pin = models.CharField(max_length=200)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
