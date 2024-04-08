from django.apps import AppConfig


class NewsServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news_service"

    def ready(self):
        import news_service.scheduler
