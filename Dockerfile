FROM python:3.12-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

# Collect static files


#EXPOSE 8000
#
## Run the app with gunicorn
#CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
