from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'app_auth'

    def ready(self):
        import app_auth.signals
