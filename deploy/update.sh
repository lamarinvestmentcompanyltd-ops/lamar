#!/usr/bin/env bash
# Run on the server after uploading new code:  /srv/lamar/app/deploy/update.sh
set -euo pipefail
cd /srv/lamar/app
set -a; source /srv/lamar/.env; set +a
/srv/lamar/venv/bin/pip install -r requirements.txt
/srv/lamar/venv/bin/python manage.py migrate --noinput
/srv/lamar/venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart lamar
