upstream luigiliu {
    server django:8000;
}

server {
    listen 80;
    server_name luigiliu.com www.luigiliu.com;
    location /.well-known/acme-challenge/ {
        root /code/certbot/www/;
    }
    location / {
        return 301 https://www.luigiliu.com$request_uri;
    }
}

server {

    listen 443 ssl;
    server_name luigiliu.com;

    ssl_certificate /etc/letsencrypt/live/luigiliu.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/luigiliu.com/privkey.pem;

    include /code/ta/certbot/conf/options-ssl-nginx.conf;
    ssl_dhparam /code/certbot/conf/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        return 301 https://www.luigiliu.com$request_uri;
    }
}
server {
    listen 443 ssl;
    server_name www.luigiliu.com;

    ssl_certificate /etc/letsencrypt/live/luigiliu.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/luigiliu.com/privkey.pem;

    include /code/certbot/conf/options-ssl-nginx.conf;
    ssl_dhparam /code/certbot/conf/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://luigiliu;
        proxy_redirect off;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /data/static/ {
        alias /code/data/static/;
    }
    location /data/media/ {
        alias /code/data/media/;
    }
}


