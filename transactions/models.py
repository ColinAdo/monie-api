from django.db import models

from accounts.models import Account
from .choices import TRANSACTION_TYPES

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=99999999, decimal_places=2)
    transaction_type = models.CharField(max_length=200, choices=TRANSACTION_TYPES)
    content = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.transaction_type
