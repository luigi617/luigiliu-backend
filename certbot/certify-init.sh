#!/bin/sh

set -e


until nc -z nginx 80; do
    echo "Waiting for nginx..."
    sleep 5s & wait ${!}
done

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroot-path "/code/certbot/www/" \
    -d "$DOMAIN" \
    -d "$SUBDOMAIN" \
    --email $ACME_DEFAULT_EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    --noninteractive \