from django.urls import re_path
from machine.consumers.machine_consumer import MachineConsumer

websocket_urlpatterns = [
    re_path(r"ws/led/$", MachineConsumer.as_asgi()),
    re_path(r"ws/machine/$", MachineConsumer.as_asgi()),
]