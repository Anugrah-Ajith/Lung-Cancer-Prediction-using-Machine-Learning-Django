"""
WSGI config for lung_cancer_project project.

It exposes the WSGI callable as a module-level variable named ``application``.
This also serves as the Vercel serverless function entry point.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lung_cancer_project.settings')

application = get_wsgi_application()

# On Vercel, /tmp/db.sqlite3 is ephemeral and lost between cold starts.
# Run migrations automatically on each cold start to ensure auth tables exist.
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    from django.db import connection
    try:
        # Check if auth_user table exists; if not, run migrations
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';"
            )
            if not cursor.fetchone():
                call_command('migrate', '--noinput')
    except Exception:
        # If anything goes wrong, try migrating anyway
        try:
            call_command('migrate', '--noinput')
        except Exception:
            pass

# Vercel entry point
app = application
