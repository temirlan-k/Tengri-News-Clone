from django.apps import AppConfig


class UserServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_service"

    def ready(self):
        try:
            import user_service.signals
        except ImportError:
            print("Import Error")
            pass
