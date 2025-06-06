from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Account

User = get_user_model()

@receiver(post_save, sender=User)
def create_account_for_new_user(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(
            user=instance,
            name='Income',  
            description="Income account"
        )
