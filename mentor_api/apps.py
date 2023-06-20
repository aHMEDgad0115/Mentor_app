from django.apps import AppConfig


class MentorApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentor_api'

    def ready(self):
        import mentor_api.api.signals