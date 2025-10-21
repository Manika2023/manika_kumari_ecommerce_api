from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    # For testing without auth
          self.group_name = "testingadmin_user_group"
          await self.channel_layer.group_add(self.group_name, self.channel_name)
          await self.accept()


    async def disconnect(self, close_code):
        # Remove this channel from the group on disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Optional: handle incoming messages from frontend (usually not needed here)
        data = json.loads(text_data)
        print("data is",data)
        await self.send(text_data=json.dumps({"message": "Received"}))

    async def order_status(self, event):
        print("📩 Received event in consumer:", event)
        # This method name corresponds to 'type': 'order_status' in group_send
        await self.send(text_data=json.dumps({
           "order_id": event["order_id"],
           "status": event["status"],
           "total_price": event.get("total_price"),
           "products": event.get("products", [])
        }))
        print("executing consumers")
