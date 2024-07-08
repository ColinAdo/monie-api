from django.conf import settings
from django.db import models

# Account model
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="accounts", on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.0, max_digits=99999999, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
