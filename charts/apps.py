from django.apps import AppConfig


class ChartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charts'
    
    def ready(self):
        from . import signals
