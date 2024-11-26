# E-learning_platform

python manage.py runserver (run Redis container before that)


About fixtures.
python manage.py dumpdata courses(name app) --indent=2(indentation) -> JSON in standart output

python manage.py dumpdata courses --indent=2 --ouput=courses/fixtures/subjects.json -> to the file

python manage.py loaddata subjects.json -> load data


Using CACHE.
docker run -it <--rm> --name memcached -p 11211:11211 memcached -m 64
-m - limit memory 64MB
Caching system can be configured using CACHES settings. In our case:
- LOCATION - the location of the cache, depends on backend(dir, host and port);
- BACKEND - cache backend.


Django Toolbar.
1. Add to INSTALLED_APPS.
2. Add to MIDDLEWARE before any other middleware, except that encodes
the response's content.
3. Add INTERNAL_IPS and add to the list your local IP (toolbar will 
only display on this IP address)

Update and FetchFrom CacheMiddleware is used to site caching, but
for our case, it's not appropriate way, because of content management
views for instructors.

If you want to use Redis cache backend, change BACKEND and LOCATION
settings on corresponding file and launch redis container:
    docker run -it <--rm> --name redis -p 6379:6379 redis
In order to monitor redist statistics, you need to install redisboard(requirements). 
On admin site you have to add URL: redis://localhost:6379/0, which
means Redis instance running on localhost, on port 6379 and uses
Redis db numbered 0.

API
Using curl for interaction.
http://127.0.0.1:8000/api/subjects/ - list of subject or + id => detail
Pagination. You can pass parameters page and page_size for test in URL like: <http://127.0.0.1:8000/api/subjects/?page=2&page_size=2>


For chat(<http://127.0.0.1:8000/chat/room/1/>) server we need:
1. Set up a consumer (read/write messages to a communication channel)
2. Configure routing (allow us to combine and stack our consumers)
3. Implement a WebSocket client (to connect to the WebSocket from browser 
and send/receive messages using JS):
- open WebSocket connection with the server when the page is loaded;
- add messages to a HTML container when data is received through the WebSocket;
- attach a listener to the submit button to send messages.
Should be HTTP .... 200;
    Websocket HANDSHAKING;
    WEBSOCKET CONNECT;
4. Enable a channel layer (allow to talk between different instances of an app). We have used Redis to implement channel layers.
Add to the settings.py CHANNEL_LAYERS setting (RedisChannelLayer backend,
host 127.0.0.1 and port 6379). Next, run the container
    docker run -it <--rm> --name redis -p 6379:6379 redis
In order to test chat, open browser another tab in private mode.



Launch app with few settings files.
To indicate the settings module that you want to use add --settings option:
    python manage.py runserver --settings=educa.settings.local
If you don't want to pass the --settings option eveery time you run 
a management command, you can define the DJANGO_SETTINGS_MODULE env
variable. For Linux execute the following command in the shell:
    export DJANGO_SETTINGS_MODULE=educa.settings.local
or for Windows:
    set DJANGO_SETTINGS_MODULE=educa.settings.local


In order to docker compose up:
1. Use wait-for-it.sh to wait for db host be ready and accept
connections on port 5432 before starting Django server.
2. Grant permission to it:
    chmod +x wait-for-it.sh
3. When you launch web and db services, you have to apply
migrations. Run the following command in the directory, where
the docker-compose.yml file is located:
    docker compose exec web python /code/educa/manage.py migrate
4. Create a superuser:
    docker compose exec web python /code/educa/manage.py createsuperuser


We will use uWSGI as a server and NGINX server in front of it
for serving static files efficiently and we will forward dynamic
requests to uWSGI workers. After implementation uWSGI with NGINX
we can access to server by <http://localhost/>, because we are
accessing the host through the standard HTTP port 80.

Add following line to /etc/hosts file:
    127.0.0.1	educaproject.com www.educaproject.com
By doing so, you are routing the upper 2 hostnames to our local
server.

We use NGINX to server static files in our production environment.
In order to collect all of static files:
1. Add STATIC_ROOT directory to base.py file.
2. docker compose up
3. docker compose exec web python /code/educa/manage.py collectstatic 
    or 
    python manage.py collectstatic --settings=educa.settings.local
Thus /static/ and /media/ paths are now served by NGINX directly,
/ path are passed by NGINX to uWSGI through the UNIX socket.


Checking.
Django includes a system check framework for valdating our project,
that inspects the applications installed in Django project and detects
common problems. Launch check:
    python manage.py check --settings=educa.settings.prod
For production deployment:
    python manage.py check --deploy --settings=educa.settings.prod


SSL/TLS
Generate SSL/TLS certificate:
    openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes \
    -keyout ssl/educa.key -out ssl/educa.crt \
    -subj '/CN=*.educaproject.com' \
    -addext 'subjectAltName=DNS:*.educaproject.com'