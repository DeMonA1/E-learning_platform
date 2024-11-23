"""
ASGI config for educa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


from chat.routing import websocket_urlpatterns

# this middleware supports standard Django auth (user details 
# store in the session)
application = ProtocolTypeRouter({'http': django_asgi_app,
                                  'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
                                  })