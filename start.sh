#!/usr/bin/env bash
# Railway start script: prepares the site, then starts the web server.
# Runs on every deploy/restart. The first-boot block runs only once.
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# First boot only: load the site content (team, partners, materials, photos)
# and create the admin login from the DJANGO_SUPERUSER_* variables.
MARKER="${RAILWAY_VOLUME_MOUNT_PATH:-.}/.lamar_initialized"
if [ ! -f "$MARKER" ]; then
  python manage.py seed_initial_data || echo "WARNING: seeding content failed - add it from /admin/"
  if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput || echo "WARNING: could not create the admin user"
  else
    echo "NOTE: DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not set - no admin user created"
  fi
  touch "$MARKER"
fi

exec gunicorn lamar_project.wsgi --workers 2 --bind "0.0.0.0:${PORT:-8000}" --access-logfile -
