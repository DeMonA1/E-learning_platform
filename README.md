# E-learning_platform

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