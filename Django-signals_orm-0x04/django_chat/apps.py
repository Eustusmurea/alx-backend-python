from django.apps import AppConfig


class MessagingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_chat'

    def ready(self):
        # Import signals to ensure they are registered
        import django_chat.signals
