#!/bin/sh
set -e

if [ ! -d "/code/staticfiles" ]; then
    sudo mkdir -p /code/staticfiles
fi

sudo chown -R appuser:appuser /code/staticfiles
sudo chmod -R 755 /code/staticfiles
echo "--> Collecting static files..."
python manage.py collectstatic --noinput

echo "--> Starting website"
exec "$@"