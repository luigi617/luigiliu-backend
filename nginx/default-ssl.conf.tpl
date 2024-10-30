# Define upstream servers
upstream django {
    server django:8000;
}

upstream react_app {
    server react_build:80;
}

# HTTP Server Block: Handles ACME challenges and redirects HTTP to HTTPS
server {
    listen 80;
    server_name luigiliu.com www.luigiliu.com;

    # Handle Let's Encrypt ACME challenges
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect all other HTTP requests to HTTPS (www)
    location / {
        return 301 https://www.luigiliu.com$request_uri;
    }
}

# HTTPS Server Block for Non-www: Redirects to www
server {
    listen 443 ssl;
    server_name luigiliu.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/luigiliu.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/luigiliu.com/privkey.pem;

    # SSL Configuration
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Enforce HTTPS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Redirect to www
    location / {
        return 301 https://www.luigiliu.com$request_uri;
    }
}

# HTTPS Server Block for www: Serves React app and proxies API to Django
server {
    listen 443 ssl;
    server_name www.luigiliu.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/luigiliu.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/luigiliu.com/privkey.pem;

    # SSL Configuration
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Enforce HTTPS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy API requests to Django
    location /api/ {
        proxy_pass http://django:8000/api/;
        proxy_redirect off;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve React frontend
    location / {
        proxy_pass http://react_app:80/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Serve static files
    location /data/static/ {
        alias /code/data/static/;
    }

    # Serve media files
    location /data/media/ {
        alias /code/data/media/;
    }
}
