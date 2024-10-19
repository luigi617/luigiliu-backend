upstream luigiliu {
    server django:8000;
}


server {

    listen 80;
    server_name www.luigiliu.com;
    
    location / {
        return 301 http://luigiliu.com;
    }

}
server {

    listen 80;
    server_name luigiliu.com;
    
    location /.well-known/acme-challenge/ {
        root /code/certbot/www/;
    }
    location /data/static/ {
        alias /code/data/static/;
    }
    location /data/media/ {
        alias /code/data/media/;
    }
    location / {
        proxy_pass http://luigiliu.com$request_uri;
        proxy_redirect off;
    }

}
