#!/usr/bin/env python3
import sys
import os
import warnings
from optparse import OptionParser

import django
from django.conf import settings
from django.core.management import call_command


def runtests(test_path="form_creator"):
    if not settings.configured:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        }

        # Configure test environment
        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=(
                "django.contrib.admin",
                "django.contrib.contenttypes",
                "django.contrib.auth",
                "django.contrib.sessions",
                "django.contrib.messages",
                "form_creator",
            ),
            ROOT_URLCONF="form_creator.urls",
            LANGUAGES=(("en", "English"),),
            MIDDLEWARE_CLASSES=(),
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
            ],
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",  # noqa E501
                    "DIRS": [os.path.join("form_creator", "templates")],
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.template.context_processors.debug",
                            "django.template.context_processors.request",
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",  # noqa E501
                        ],
                    },
                },
            ],
            SECRET_KEY="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
        )

    django.setup()
    warnings.simplefilter("always", DeprecationWarning)
    failures = call_command(
        "test", test_path, interactive=False, failfast=False, verbosity=1
    )

    sys.exit(bool(failures))


if __name__ == "__main__":
    parser = OptionParser()

    (options, args) = parser.parse_args()
    runtests(*args)
