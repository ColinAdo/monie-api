from django.db import models

from accounts.models import Account
from auths.models import CustomUser

# Transaction model
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=7)
    description = models.CharField(max_length=34, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.transaction_type
