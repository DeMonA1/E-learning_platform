from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    # pattern course_id any digits one or more in the end
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', 
            consumers.ChatConsumer.as_asgi()),
]