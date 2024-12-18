from django.apps import AppConfig

class MyshopDjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myshop_dj'

    def ready(self):
        import myshop_dj.signals