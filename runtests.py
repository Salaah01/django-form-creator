#!/usr/bin/env python3
import sys
import warnings
from optparse import OptionParser

import django
from django.conf import settings
from django.core.management import call_command


def runtests(test_path='form_creator'):
    if not settings.configured:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }

        # Configure test environment
        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=(
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'form_creator',
            ),
            ROOT_URLCONF=None,
            LANGUAGES=(('en', 'English'),),
            MIDDLEWARE_CLASSES=(),
        )

    django.setup()
    warnings.simplefilter('always', DeprecationWarning)
    failures = call_command(
        'test',
        test_path,
        interactive=False,
        failfast=False,
        verbosity=1
    )

    sys.exit(bool(failures))


if __name__ == '__main__':
    parser = OptionParser()

    (options, args) = parser.parse_args()
    runtests(*args)
