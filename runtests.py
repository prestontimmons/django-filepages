#!/usr/bin/env python

from os.path import dirname, abspath
import sys

from django.conf import settings


if not settings.configured:
    settings_dict = dict(
        INSTALLED_APPS=["filepages", "test_filepages"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            },
        },
    )

    settings.configure(**settings_dict)


def runtests():
    test_args = ["test_filepages"]
    sys.path.insert(0, dirname(abspath(__file__)))

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(
        verbosity=1,
        interactive=True,
        failfast=False,
    ).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests()
