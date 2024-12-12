import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.models import Account
import logging

# Account consumer
class AccountConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
            return

        self.username = user.username
        async_to_sync(self.channel_layer.group_add)(
            self.username, self.channel_name
        )
        self.accept()
        logging.info(f'User connected to room: {self.username}')
        print(f"{self.username} connected")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.username, self.channel_name
        )
        logging.info(f"User disconnected from room: {self.username}")
        print(f"{self.username} disconnected")

    def receive(self, text_data):
        # Parse the received JSON data
        data = json.loads(text_data)
        print("Received", json.dumps(data, indent=2))


        account_name = data['data']['name']
        description = data['data']['description']
        amount = data['data']['amount']

        # Save account data to the database
        account = Account.objects.create(
            name=account_name,
            description=description,
            amount=amount,
            user=self.scope['user']
        )

        # Send the message to the group
        self.channel_layer.group_send(
            self.username,
            {
                'type': 'account_message',
                'name': account_name,
                'description': description,
                'amount': amount,
            }
        )

    def account_message(self, event):
        # Send the message to WebSocket
        name = event['name']
        description = event['description']
        amount = event['amount']

        self.send(text_data=json.dumps({
            'name': name,
            'description': description,
            'amount': amount,
        }))
