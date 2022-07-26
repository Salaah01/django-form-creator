from django.db import connection
from django.core.checks import Warning, register
from django.contrib.contenttypes.models import ContentType


def is_content_types_loaded() -> bool:
    """Returns True if the contenttypes app is loaded."""
    return ContentType._meta.db_table in connection.introspection.table_names()


@register()
def check_content_types_is_loaded(app_configs, **kwargs):
    warnings = []
    if not is_content_types_loaded():
        warnings.append(
            Warning(
                "ContentTypes table is not loaded.",
                hint="Run migrations",
                obj="django-form-creator",
            )
        )
    return warnings
