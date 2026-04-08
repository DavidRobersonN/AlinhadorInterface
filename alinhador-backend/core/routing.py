from django.urls import re_path
from .consumers import LedConsumer

websocket_urlpatterns = [
    re_path(r'ws/led/$', LedConsumer.as_asgi()),
]