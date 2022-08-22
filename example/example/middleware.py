from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User


def react_dev_auto_login_middleware(get_response):
    """If the requests are arriving on the react development port, the
    application is being run on DEBUG mode and the user is not logged in, then
    log them in.
    """

    def middleware(request):
        # Check the port in which the request is coming from.
        if not request.user.is_authenticated and request.META.get(
            "HTTP_ORIGIN",
            "",
        ).split(":")[-1] == str(settings.REACT_DEV_PORT):
            user, created = User.objects.get_or_create(
                username="react_dev",
            )
            if created:
                user.set_password("react_dev")
                user.save()
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)

        return get_response(request)

    return middleware


class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
        return self.get_response(request)
