import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ItineraryConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time itinerary collaboration and voting."""

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"itinerary_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return

        message = data.get("message")
        if not message:
            await self.send(
                text_data=json.dumps({"error": "Missing 'message' field"})
            )
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "itinerary_update",
                "message": message,
            },
        )

    async def itinerary_update(self, event):
        await self.send(
            text_data=json.dumps({"message": event["message"]})
        )
