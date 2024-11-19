# 3 options to use model inheritance in Django
# 1 - Abstract model
from django.db import models
from django.utils import timezone


# NO TABLE in db for this class; Abstract class
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

# Table will be created for this class
class Text(BaseContent):
    body = models.TextField()



# 2 - Multi-table inheritance
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

# basecontent_ptr_id field will be created, 
# which point to BaseContent table in db
class Text(BaseContent):
    body = models.TextField()



# 3 - Proxy models
# ONE TABLE will be created and both clasess can operate it
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class OrderedContent(BaseContent):
    class Meta:
        proxy = True
        ordering = ['created']
    
    def created_delta(self):
        return timezone.now() - self.created
    


from django.contrib.auth.models import User
from courses.models import Subject, Course, Module

user = User.objects.last()
subject = Subject.objects.last()
c1 = Course.objects.create(subject=subject, owner=user, title=
                           'Course 1', slug='course1')
m1 = Module.objects.create(course=c1, title='Module 1')
m1.order  # 0

m2 = Module.objects.create(course=c1, title='Module 2')
m2.order  # 1

m3 = Module.objects.create(course=c1, title='Module 3', order=5)
m3.order    # 5

m4 = Module.objects.create(course=c1, title='Module 4')
m4.order    # 6

c2 = Course.objects.create(subject=subject, title='Course 2', 
                           slug='course2', owner=user)
m5 = Module.objects.create(course=c2, title='Module 1')
m5.order



from courses.models import Module
Module.objects.latest('id').id      # 9



# CACHE
# memcached should be launched
from django.core.cache import cache
cache.set('musician', 'Django', 20)
cache.get('musician')

# cache a queryset
from courses.models import Subject
subjects = Subject.objects.all()
cache.set('my_subjects', subjects)



# serializer (DRF)
from courses.models import Subject
from courses.api.serializers import SubjectSerializer
subject = Subject.objects.latest('id')
serializer = SubjectSerializer(subject)
serializer.data

# parse data
from io import BytesIO
from rest_framework.parsers import JSONParser
data = b'{"id": 4, "title": "Programming", "slug": "programming"}'
JSONParser().parse(BytesIO(data))

# render data
from rest_framework.renderers import JSONRenderer
JSONRenderer().render(serializer.data)