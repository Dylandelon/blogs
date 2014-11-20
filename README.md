blogs
=====

Blogs writing by markdown. Serves by [Pelican][1].

[1]: https://github.com/getpelican/pelican


## Install the dependencies

    :::shell
    sudo pip install -r requirements.txt

## Install nginx

    :::shell
    sudo apt-get install nginx-full

## Config nginx

    :::shell
    sudo vim /etc/nginx/sites-enabled/default

    server {
        listen 80 default_server;
        server_name localhost;
        root /home/kamidox/lab/blogs/output;

        location / {
            index index.html;
        }
    }
