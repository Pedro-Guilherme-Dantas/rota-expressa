from django.apps import AppConfig


class RotaExpressaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rota_expressa'

    def ready(self):
        import rota_expressa.signals
