#!/bin/sh
set -e

# Ensure directories exist
mkdir -p /code/staticfiles
mkdir -p /code/media

chown -R appuser:appuser /code/staticfiles /code/media
chmod -R 755 /code/staticfiles /code/media
echo "--> Collecting static files..."
python manage.py collectstatic --noinput

echo "--> Starting website"

# Start Gunicorn in background
gunicorn config.wsgi:application --bind "0.0.0.0:8000" &

echo "starting nginx server"
# Start Nginx in foreground
nginx -g 'daemon off;'

