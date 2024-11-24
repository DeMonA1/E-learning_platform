from django.conf import settings
from django.db import models

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    # user can't be deleted if related messages exist
                             on_delete=models.PROTECT,
                             related_name='chat_messages')
    course = models.ForeignKey('courses.Course',
                               on_delete=models.PROTECT,
                               related_name='chat_messages')
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} on {self.course} at {self.sent_on}'

