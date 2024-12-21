import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Account

# Account consumer
class AccountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
            return

        self.username = user.username
        await self.channel_layer.group_add(
            self.username, 
            self.channel_name
        )
        await self.accept()
        logging.info(f'User connected to room: {self.username}')
        print(f"{self.username} connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.username, 
            self.channel_name
        )
        logging.info(f"User disconnected from room: {self.username}")
        print(f"{self.username} disconnected")

    # Parse the received JSON data
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received", json.dumps(data, indent=2))

        account_name = data['data']['name']
        description = data['data']['description']
        amount = data['data']['amount']

        # Send the message to the group
        await self.channel_layer.group_send(
            self.username,
            {
                'type': 'account_message',
                'name': account_name,
                'description': description,
                'amount': amount
            }
        )

        await self.save_account(account_name, description, amount)

    # Send the message to WebSocket
    async def account_message(self, event):
        name = event['name']
        description = event['description']
        amount = event['amount']

        await self.send(text_data=json.dumps({
            'name': name,
            'description': description,
            'amount': amount,
        }))


    @sync_to_async
    def save_account(self, account_name, description, amount):
        user = self.scope.get('user')

        Account.objects.create(name=account_name, description=description, amount=amount, user=user)
