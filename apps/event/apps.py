from django.apps import AppConfig


class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.event'
    test = True

    def ready(self):
        if self.test:
            return

        import apps.event.signals
