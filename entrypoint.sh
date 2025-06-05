#!/bin/sh
echo "--> Collecting static files..."
python manage.py collectstatic --noinput

echo "--> Starting website"
exec "$@"