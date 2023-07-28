from django.apps import AppConfig


class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.event'

    def ready(self):
        # Makes sure all signal handlers are connected
        from . import handlers # noqa