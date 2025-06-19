from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.utils import OperationalError, ProgrammingError
import os

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name != 'auths':
        return
    User = get_user_model()
    try:
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123')

            print(f"🔐 Creating superuser: {username}")
            User.objects.create_superuser(username=username, email=email, password=password)
    except (OperationalError, ProgrammingError) as e:
        print(f"❗ Error creating superuser: {e}")