import json

from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.core.exceptions import ValidationError
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
        self.channel_layer.group_add(
            self.username, self.channel_name
        )
        self.accept()
        logging.info(f'User connected to room: {self.username}')
        print(f"{self.username} connected")

    def disconnect(self, close_code):
       self.channel_layer.group_discard(
            self.username, self.channel_name
        )
       print(f"{self.username} disconnected")


    def receive(self, text_data):
        # Parse the received JSON data
        data = json.loads(text_data)
        account_name = data.get("name")
        description = data.get("description")
        amount = data.get("amount")

        self.channel_layer.group_send(
            self.username,
            {
                'type': 'chat_message',
                'name': account_name,
                'description': description,
                'amount': amount,
            }
            )
        # self.save_account(account_name, description, amount)
        account = Account.objects.create(
            name=account_name,
            description=description,
            amount=amount,
            user=self.scope['user']
        )


    # Sending messages
    def account_message(self, event):
        name = event['name']
        description = event['description']
        amount = event['amount']

        self.send(text_data=json.dumps({
            'name': name,
            'description': description,
            'amount': amount,
        }))

    # @sync_to_async
    # def save_account(self, name, description, amount):
    #     user = self.scope['user']

    #     # Create a new Account instance
    #     Account.objects.create(user=user, name=name, description=description, amount=amount)
    
    