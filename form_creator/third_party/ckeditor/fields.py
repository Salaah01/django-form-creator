try:
    from ckeditor.fields import RichTextField
except ImportError:
    from django.db.models import TextField as RichTextField


__all__ = ["RichTextField"]
