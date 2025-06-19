from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.conf import settings
import os


class AuthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auths'

    def ready(self):
        from django.dispatch import receiver
        from django.db.utils import OperationalError, ProgrammingError

        @receiver(post_migrate)
        def create_superuser(sender, **kwargs):
            User = get_user_model()
            try:
                if not User.objects.filter(is_superuser=True).exists():
                    User.objects.create_superuser(
                        username=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
                        email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
                        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123')
                    )
            except (OperationalError, ProgrammingError):
                # Tables might not be ready yet — safe to ignore
                pass
