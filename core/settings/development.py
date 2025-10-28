from .base import *

DEVELOP_APP = [
    "debug_toolbar"
]

DEVELOP_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += DEVELOP_APP

MIDDLEWARE += DEVELOP_MIDDLEWARE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]
