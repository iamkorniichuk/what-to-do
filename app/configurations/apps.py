from django.apps import AppConfig


class ConfigurationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "configurations"

    def ready(self):
        from .signals import create_configuration as create_configuration

        return super().ready()
