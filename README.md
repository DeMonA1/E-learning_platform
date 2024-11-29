# E-learning_platform

> [!TIP]
> [Main Django commands](https://github.com/DeMonA1/MyBlog__Django/blob/main/README.md#diamonds-basic-django-commands)

## :hammer_and_pick: Launch service
1. [Redis (docker container)](https://github.com/DeMonA1/Shop/blob/main/README.md#redis):
```
 docker run --it --name redis -p 6379:6379 redis
```
2. Launch app with few settings files.
To indicate the settings module that you want to use add ***--settings*** option:
```
python manage.py runserver --settings=educa.settings.local
```
If you don't want to pass the ***--settings*** option eveery time you run 
a management command, you can define the ***DJANGO_SETTINGS_MODULE*** env
variable. For Linux execute the following command in the shell:
```
export DJANGO_SETTINGS_MODULE=educa.settings.local
```
or for Windows:
```
set DJANGO_SETTINGS_MODULE=educa.settings.local
```

> You can get access by <http://127.0.0.1:8000> or <https://(www).educaproject.com>(on compose),
> as well as by a subdomain (in compose).


## :notebook_with_decorative_cover: About fixtures.
- Generate JSON serialized data:
```
python manage.py dumpdata courses(name app) --indent=2(indentation)
```
- If you want to save data in the specific file:
```
python manage.py dumpdata courses --indent=2 --ouput=courses/fixtures/subjects.json
```
- In order to load data from JSON ot DB:
```
python manage.py loaddata subjects.json
```

## :gear: Necessary services
### :card_file_box: Cache
<ins>***Memcached***</ins>
You can use for cache Memcached, run it as follow:
```
docker run -it <--rm> --name memcached -p 11211:11211 memcached -m 64
```
> -m => limit memory 64MB

Caching system can be configured using ***CACHES*** settings. In our case:
- LOCATION - the location of the cache, depends on backend(dir, host and port);
- BACKEND - cache backend.

<ins>***Redis***</ins>
If you want to use Redis cache backend, change ***BACKEND*** and ***LOCATION***
settings on corresponding file and launch redis container:
```
    docker run -it <--rm> --name redis -p 6379:6379 redis
```
In order to monitor redis statistics, you need to install redisboard(requirements). 
On admin site you have to add URL: <ins>***redis://localhost:6379/0***</ins>, which
means Redis instance running on localhost, on port 6379 and uses
Redis db numbered 0.

### :wrench: Django Toolbar.
1. Add to ***INSTALLED_APPS***.
2. Add to ***MIDDLEWARE*** before any other middleware, except that encodes
the response's content.
3. Add ***INTERNAL_IPS*** and add to the list your local IP (toolbar will 
only display on this IP address)
> [!NOTE]
> UpdateCacheMiddleware and FetchFromCacheMiddleware is used to site caching, but
> for our case, it's not appropriate way, because of content management
> views for instructors.

### NGINX and uWSGI
We will use ***uWSGI*** as a server and ***NGINX*** server in front of it
for serving static files efficiently and we will forward dynamic
requests to uWSGI workers. After implementation uWSGI with NGINX
we can access to server by <http://localhost/>, because we are
accessing the host through the standard HTTP port 80.

Add following line to <ins>***/etc/hosts***</ins> file:
```
127.0.0.1	educaproject.com www.educaproject.com
```
By doing so, you are routing the upper 2 hostnames to our local
server.

We use NGINX to server static files in our production environment.
In order to collect all of static files:
1. Add ***STATIC_ROOT*** directory to the ***base.py*** file.
2.```
docker compose up```
4. docker compose exec web python /code/educa/manage.py collectstatic 
    or 
    python manage.py collectstatic --settings=educa.settings.local
Thus /static/ and /media/ paths are now served by NGINX directly,
/ path are passed by NGINX to uWSGI through the UNIX socket.

## About API
- Using curl for interaction.
- http://127.0.0.1:8000/api/subjects/ - list of subject or + id => detail
- Pagination. You can pass parameters ***page*** and ***page_size*** for test in URL like:
<http://127.0.0.1:8000/api/subjects/?page=2&page_size=2>

## About Chat server
For chat(<http://127.0.0.1:8000/chat/room/1/>) server we need:
1. Set up a consumer (read/write messages to a communication channel)
2. Configure routing (allow us to combine and stack our consumers)
3. Implement a WebSocket client (to connect to the WebSocket from browser 
and send/receive messages using JS):
- open WebSocket connection with the server when the page is loaded;
- add messages to a HTML container when data is received through the WebSocket;
- attach a listener to the submit button to send messages.
> [!NOTE]
> Should be HTTP .... 200;
> 
>    Websocket HANDSHAKING;
>
>    WEBSOCKET CONNECT;
4. Enable a channel layer (allow to talk between different instances of an app). We have used Redis to implement channel layers.
Add to the ***settings.py*** **CHANNEL_LAYERS** setting ('BACKEND': 'channels_redis.core.RedisChannelLayer',
'CONFIG': {'hosts': [('127.0.0.1', 6379)). Next, run the container as follows:
```
    docker run -it <--rm> --name redis -p 6379:6379 redis
```
- [x] In order to test chat, open browser another tab in private mode.

## Docker compose
In order to docker compose up:
1. Use <ins>***wait-for-it.sh***</ins> to wait for db host be ready and accept
connections on port 5432 before starting Django server.
2. Grant permission to it:
```
chmod +x wait-for-it.sh
```
3. When you launch web and db services, you have to apply
migrations. Run the following command in the directory, where
the ***docker-compose.yml*** file is located:
```
docker compose exec web python /code/educa/manage.py migrate
```
4. Create a superuser:
```
docker compose exec web python /code/educa/manage.py createsuperuser
```




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


Subdomain (subdomain.educaproject.com)
For testing custom middleware with a Course object with the slug first,
add the following line to /etc/hosts file:
    127.0.0.1 first.educaproject.com


Send masss reminder to users by email.
In order to make Django output emails to the standard ouput during
development, add it to base.py file:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
Management command in container:
    docker compose exec web python /code/educa/manage.py \
    enroll_reminder --days=20 --settings=educa.settings.prod
We can run management commands from code as follows:
    from django.core import management
    management.call_command('enroll_reminder', days=20)
Django management command can be scheduled to run automatically
using cron or Celery Beat.

For local tests, you need to comment subdomain_course_middleware in 
MIDDLEWARE constant in base.py settings file.
