from django.apps import AppConfig


class TrainingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.trainings"
    label = "trainings"

    def ready(self):
        pass
