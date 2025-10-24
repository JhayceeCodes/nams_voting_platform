from .base import *
import os

DEBUG = False

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOW_ALL_ORIGINS = False

frontend_urls = os.getenv("FRONTEND_URLS", "")
if frontend_urls:
    CORS_ALLOWED_ORIGINS = [url.strip().rstrip('/') for url in frontend_urls.split(",")]
    CSRF_TRUSTED_ORIGINS = [url.strip().rstrip('/') for url in frontend_urls.split(",")]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

CORS_ALLOW_CREDENTIALS = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
