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
exec python manage.py runserver 0.0.0.0:8000
# exec gunicorn config.wsgi:application \
#     --workers=3 \
#     --worker-class=gevent \
#     --bind=0.0.0.0:8000 \
#     --timeout=120 \
#     --keep-alive=5 \
#     --log-level=info
