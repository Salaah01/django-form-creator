from django.contrib.contenttypes.models import ContentType


def get_content_type_from_dict(value: dict) -> ContentType:
    """Given a dictionary that may contain `id` or `app_label` and `model`
    keys, return a `ContentType` instance.
    """
    ct_id = value.get("id")
    if ct_id:
        return ContentType.objects.get_for_id(ct_id)
    else:
        return ContentType.objects.get_by_natural_key(
            app_label=value["app_label"],
            model=value["model"],
        )
