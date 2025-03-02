from django.apps import AppConfig

class TechnewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'technews'
    
    def ready(self):
        from . import scheduler
        scheduler.start()
