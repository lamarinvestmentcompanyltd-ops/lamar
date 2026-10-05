#!/usr/bin/env bash
# Nightly backup of the database + uploaded photos. Add to cron:
#   0 2 * * * /srv/lamar/app/deploy/backup.sh
set -euo pipefail
DEST=/srv/lamar/backups; mkdir -p "$DEST"
STAMP=$(date +%F)
sqlite3 /var/lib/lamar/db.sqlite3 ".backup '$DEST/db-$STAMP.sqlite3'"
tar -czf "$DEST/media-$STAMP.tar.gz" -C /var/lib/lamar media
find "$DEST" -type f -mtime +30 -delete      # keep 30 days
# Also copy $DEST off the server (another machine / cloud drive) - a backup on the same disk is not enough.
