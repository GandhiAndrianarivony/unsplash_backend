from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
import environ


env = environ.Env()

os.environ.setdefault(env("DJANGO_SETTINGS_MODULE"), "infinix.settings.base")

app = Celery(
    "infinix",
    include=["apps.images.tasks"],
)
app.config_from_object("django.conf:settings", namespace="CELERY")
