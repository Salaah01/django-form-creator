from django import template
from django.contrib.auth import get_user_model
from .. import models as fc_models

User = get_user_model()
register = template.Library()


@register.filter
def can_edit_form(form: fc_models.Form, user: User) -> bool:
    """Check if the user can edit the form."""
    return form.can_edit(user)


@register.filter
def can_delete_form(form: fc_models.Form, user: User) -> bool:
    """Check if the user can delete the form."""
    return form.can_delete(user)


@register.filter
def can_complete_form(form: fc_models.Form, user: User) -> bool:
    """Check if the user can complete the form."""
    return form.can_complete_form(user)


@register.simple_tag
def form_completed_on(form: fc_models.Form, user: User) -> str:
    """Get the date the user completed the form."""
    responder = form.completed_by(user)
    if responder:
        return responder.created_dt.strftime("%Y-%m-%d")
    return ""
