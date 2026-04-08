import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serial_manager import send_command_to_arduino


class LedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("led_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("led_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get("command")

        if command == "ON":
            send_command_to_arduino("ON")
        elif command == "OFF":
            send_command_to_arduino("OFF")
        elif command == "TOGGLE":
            send_command_to_arduino("TOGGLE")

    async def led_status(self, event):
        await self.send(text_data=json.dumps({
            "type": "led_status",
            "state": event["state"]
        }))