from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CarStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('car_status', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the client from the 'car_status' group
        await self.channel_layer.group_discard('car_status', self.channel_name)

    async def car_status_changed(self, event):
        car_data = event['message']
        await self.send(text_data=json.dumps(car_data))