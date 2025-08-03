from django.apps import AppConfig


class MessagingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        # Import signals to ensure they are registered
        import messaging.signals
