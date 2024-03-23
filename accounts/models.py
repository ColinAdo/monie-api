from django.conf import settings
from django.db import models

from accounts.choices import TRANSACTION_TYPES

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="accounts", on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.0, max_digits=99999999, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=99999999, decimal_places=2)
    transaction_type = models.CharField(max_length=200, choices=TRANSACTION_TYPES)
    content = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.transaction_type

