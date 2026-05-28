from django.apps import AppConfig


class ComplaintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'complaints'
    def ready(self):                  # this runs when Django starts
        import complaints.signals