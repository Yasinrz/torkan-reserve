#!/bin/sh
set -e

# Ensure directories exist
mkdir -p /code/staticfiles
mkdir -p /code/media

sudo chown -R appuser:appuser /code/staticfiles /code/media
sudo chmod -R 755 /code/staticfiles /code/media
echo "--> Collecting static files..."
python manage.py collectstatic --noinput

echo "--> Starting website"
exec "$@"