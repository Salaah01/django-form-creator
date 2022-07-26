from django.apps import AppConfig


class FormCreatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "form_creator"
    verbose_name = "Form Creator"

    def ready(self):
        from . import signals

        signals.connect_seq_no_signals()
