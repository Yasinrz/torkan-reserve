FROM python:3.12-alpine3.22

# Python و Nginx
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    nginx \
    bash \
    curl

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Configure Nginx
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# exposing nginx port
EXPOSE 80


# copy entrypoint
COPY ./entrypoint.sh .

# make our entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# execute our entrypoint.sh file
CMD ["./entrypoint.sh"]