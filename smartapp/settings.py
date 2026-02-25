import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-fallback-key-do-not-use-in-prod")

# Convert "True" string to boolean
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # your app
    "core",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "smartapp.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "smartapp.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Enable WhiteNoise storage for efficient static file serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------
# SECURITY HARDENING
# ---------------------------
if not DEBUG:
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # SSL Redirect
    SECURE_SSL_REDIRECT = True
    
    # Cookie Security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # XSS Protection
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Auth Redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"
