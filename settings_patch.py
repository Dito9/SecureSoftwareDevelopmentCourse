# ─────────────────────────────────────────────────────────────────────────────
# CAMBIOS A APLICAR EN web_project/settings.py
# Agregar 'vulnerable_app' a INSTALLED_APPS y ajustar ALLOWED_HOSTS para CI
# ─────────────────────────────────────────────────────────────────────────────

# 1. En INSTALLED_APPS, agregar al final:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vulnerable_app',  # ← AGREGAR ESTA LÍNEA
]

# 2. Reemplazar ALLOWED_HOSTS para soportar CI/CD local y Render:
import os
ALLOWED_HOSTS = [
    'securesoftwaredevelopmentcourse.onrender.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]
# Si la variable de entorno DJANGO_ALLOWED_HOSTS está definida (en CI),
# agregar esos hosts también:
_extra_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if _extra_hosts:
    ALLOWED_HOSTS += [h.strip() for h in _extra_hosts.split(',') if h.strip()]
