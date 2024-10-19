#!/bin/bash
set -e

# data_path="/certbot"



# if [ ! -f "$data_path/conf/options-ssl-nginx.conf" ]; then
#   echo "### Downloading options-ssl-nginx.conf ..."
#   curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
#   echo
# fi

# if [ ! -f "$data_path/conf/ssl-dhparams.pem" ]; then
#   echo "### Downloading ssl-dhparams.pem ..."
#   curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
#   echo
# fi

export host=\$host
export request_uri=\$request_uri

echo "Checking for fullchain.pem"
# envsubst < /etc/nginx/conf.d/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf

if [ ! -e "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
  echo "No SSL cert, enabling HTTP only..."
  envsubst < /etc/nginx/conf.d/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
  echo "SSL cert exists, enabling HTTPs..."
  # envsubst < /etc/nginx/conf.d/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi

nginx -g "daemon off;"
