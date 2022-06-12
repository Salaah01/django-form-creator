from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from . import models as fc_models


def with_form(can_edit=False, can_delete=False):
    """Using the `pk` and `slug` parameters, retrieve the form.
    If the user is not allowed to see the form, raise a PermissionDenied.
    If the form does not exist, raise a 404.

    :param can_edit: If True, the user must be allowed to edit the form.
    :type can_edit: bool
    :param can_delete: If True, the user must be allowed to delete the form.
    :type can_delete: bool
    """

    def decorator(func):
        @wraps(func)
        def wrapper(
            request: HttpRequest,
            pk: int,
            slug: str,
            *args,
            **kwargs,
        ) -> HttpResponse:
            """Replaces the `pk` and `slug` parameters with the form object.

            :param request: The request object.
            :param type: HttpRequest
            :param pk: The primary key of the form.
            :param type: int
            :param slug: The slug of the form.
            :param type: str
            :param args: The positional arguments of the wrapped function.
            :param kwargs: The keyword arguments of the wrapped function.
            :return: The original function with the form object as the
                parameter replacing the `pk` and `slug` parameters.
            :rtype: HttpResponse
            """

            form = get_object_or_404(fc_models.Form, pk=pk, slug=slug)
            if can_edit and not form.can_edit(request.user):
                raise PermissionDenied
            if can_delete and not form.can_delete(request.user):
                raise PermissionDenied

            return func(request, form, *args, **kwargs)

        return wrapper

    return decorator
