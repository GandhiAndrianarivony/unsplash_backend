"""Dev Configuration"""

import environ

from .base import *


env = environ.Env()


SECRET_KEY = env("SECRET_KEY")

CORS_ALLOWED_ORIGIN = ["http://127.0.0.1:8000", "http://localhost:8000"]
