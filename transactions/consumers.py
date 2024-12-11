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
        print(f"{self.username} disconnected")


    def receive(self, text_data):
        # Parse the received JSON data
        data = json.loads(text_data)
        account_name = data.get("name")
        description = data.get("description")
        amount = data.get("amount")

        # Create a new Account instance
        account = Account.objects.create(
            name=account_name,
            description=description,
            amount=amount,
            user=self.scope['user']
        )

        # Send a success response
        self.send(json.dumps({
            "status": "success",
            "message": f"Account '{account_name}' created successfully!",
            "account_id": account.id
        }))
    
    