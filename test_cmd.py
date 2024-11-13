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