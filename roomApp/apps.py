from django.apps import AppConfig

class RoomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roomApp'

    def ready(self):
        import roomApp.signals

