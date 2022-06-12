from django import template
from django.contrib.auth import get_user_model
from .. import models as fc_models

User = get_user_model()
register = template.Library()


@register.simple_tag
def can_edit_form(form: fc_models.Form, user: User) -> bool:
    """Indicates whether the user can edit the form."""
    return form.can_edit(user)


@register.simple_tag
def can_delete_form(form: fc_models.Form, user: User) -> bool:
    """Indicates whether the user can delete the form."""
    return form.can_delete(user)
