FROM python:3.12-alpine3.22 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine3.22

RUN apk add --no-cache sudo
RUN adduser -D appuser && \
    mkdir /code && \
    mkdir -p /code/staticfiles && \
    chown -R appuser:appuser /code && \
    chmod -R 755 /code && \

echo 'appuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /code
COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code/staticfiles && \
    chown -R appuser:appuser /code/staticfiles && \
    chmod -R 755 /code/staticfiles

USER appuser

# Collect static files
COPY --chown=appuser:appuser entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

EXPOSE 8000

# Run the app with Daphne (ASGI)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "config.wsgi:application"]