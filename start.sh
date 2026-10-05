#!/usr/bin/env bash
# Railway start script: prepares the site, then starts the web server.
# Runs on every deploy/restart. The seed block runs only once.
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# First boot only: load the site content (team, partners, materials, photos).
MARKER="${RAILWAY_VOLUME_MOUNT_PATH:-.}/.lamar_initialized"
if [ ! -f "$MARKER" ]; then
  python manage.py seed_initial_data || echo "WARNING: seeding content failed - add it from /admin/"
  touch "$MARKER"
fi

# Every deploy: make sure the admin login from the DJANGO_SUPERUSER_* variables works.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell <<'PY' || echo "WARNING: could not create or update the admin user"
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

user, created = User.objects.get_or_create(username=username, defaults={"email": email})
user.is_staff = True
user.is_superuser = True
if email and not user.email:
    user.email = email
user.set_password(password)
user.save()
print(("Created" if created else "Updated") + " admin user: " + username)
PY
else
  echo "NOTE: DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not set - no admin user created"
fi

exec gunicorn lamar_project.wsgi --workers 2 --bind "0.0.0.0:${PORT:-8000}" --access-logfile -
