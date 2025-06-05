from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os


class AuthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auths'

    def ready(self):
        from django.db.utils import OperationalError
        try:
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username=os.environ.get('DJANGO_SUPERUSER_USERNAME'),
                    email=os.environ.get('DJANGO_SUPERUSER_EMAIL'),
                    password=os.environ.get('DJANGO_SUPERUSER_PASSWORD')
                )
                print("✅ Superuser created.")
        except OperationalError:
            pass
