from django.apps import AppConfig


class AuthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auths'

    def ready(self):
        import auths.signals 
