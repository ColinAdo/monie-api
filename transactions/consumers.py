import json
import logging
from decimal import Decimal

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Account
from transactions.models import Transaction
from django.conf import settings

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

        if settings.DEBUG:
            print("Received", json.dumps(data, indent=2))

        operation = data['event']
        

        # Send the message to the group if create_account oppereation
        if operation == 'create_account':
            account_name = data['data']['accountName']
            description = data['data']['description']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'create_account',
                    'name': account_name,
                    'description': description,
                }
            )
            await self.save_account(account_name, description)
        # Send the message to the group if update_account oppereation
        elif operation == 'update_account':
            account_id = data['data']['id']
            account_name = data['data']['accountName']
            description = data['data']['description']
            
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'update_account',
                    'name': account_name,
                    'description': description,
                    'id': account_id
                }
            )
            await self.save_updated_account(account_id, account_name, description)

        # Send the message to the group if delete account oppereation
        elif operation == 'delete_account':
            account_id = data['id']
            user = self.scope.get('user')

            try:
                # Fetch the transaction and related fields in a synchronous-safe manner
                account = await sync_to_async(Account.objects.get)(id=account_id, user=user)

                # Access related fields safely
                description = account.description
                amount = str(account.amount) 
                account_name = account.name
            except Account.DoesNotExist:
                logging.error(f"Account with ID {account_id} does not exist.")
                return

            # Perform the group send
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'delete_account',
                    'description': description,
                    'amount': amount,  
                    'account_name': account_name
                }
            )

            await self.save_delete_account(account_id)

        # Send the message to the group if create_transaction operation
        elif operation == 'create_transaction':
            transaction_type = data['data']['transactionType']
            account_name = data['data']['accountName']
            description = data['data']['description']
            amount = data['data']['amount']

            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'create_transaction',
                    'transaction_type': transaction_type,
                    'description': description,
                    'amount': amount,
                    'account_name': account_name
                }
            )
            await self.save_transaction(account_name, transaction_type, description, amount)
        
        # Send the message to the group if delete_transaction operation
        elif operation == 'delete_transaction':
            transaction_id = data['id']

            try:
                # Fetch the transaction and related fields in a synchronous-safe manner
                transaction = await sync_to_async(Transaction.objects.select_related('account').get)(id=transaction_id)

                # Access related fields safely
                transaction_type = transaction.transaction_type
                description = transaction.description
                amount = str(transaction.amount) 
                account_name = transaction.account.name
            except Transaction.DoesNotExist:
                logging.error(f"Transaction with ID {transaction_id} does not exist.")
                return

            # Perform the group send
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'delete_transaction',
                    'transaction_type': transaction_type,
                    'description': description,
                    'amount': amount,  
                    'account_name': account_name
                }
            )

            await self.save_delete_transaction(transaction_id)

    # Send the created account to WebSocket
    async def create_account(self, event):
        name = event['name']
        description = event['description']

        await self.send(text_data=json.dumps({
            'name': name,
            'description': description,
        }))

     # Send the updated account to WebSocket
    async def update_account(self, event):
        name = event['name']
        description = event['description']

        await self.send(text_data=json.dumps({
            'name': name,
            'description': description,
        }))

    # Send the deleted account to WebSocket
    async def delete_account(self, event):
        account_name = event['account_name']
        description = event['description']
        amount = event['amount']

        await self.send(text_data=json.dumps({
            'account_name': account_name,
            'description': description,
            'amount': amount,
        }))

    # Send the created transaction to WebSocket
    async def create_transaction(self, event):
        account_name = event['account_name']
        description = event['description']
        transaction_type = event['transaction_type']
        amount = event['amount']

        await self.send(text_data=json.dumps({
            'transaction_type': transaction_type,
            'account_name': account_name,
            'description': description,
            'amount': amount,
        }))

    # Send the deleted transaction to WebSocket
    async def delete_transaction(self, event):
        account_name = event['account_name']
        description = event['description']
        transaction_type = event['transaction_type']
        amount = event['amount']

        await self.send(text_data=json.dumps({
            'transaction_type': transaction_type,
            'account_name': account_name,
            'description': description,
            'amount': amount,
        }))

    @sync_to_async
    def save_account(self, account_name, description):
        user = self.scope.get('user')

        Account.objects.create(name=account_name, description=description, user=user)

    @sync_to_async
    def save_updated_account(self, account_id, account_name, description):
        try:
            account = Account.objects.get(id=account_id, user=self.scope.get('user'))
            account.name = account_name
            account.description = description
            account.save()
        except Account.DoesNotExist:
            logging.error(f"Account with ID {account_id} does not exist or does not belong to the user.")

    @sync_to_async
    def save_delete_account(self, account_id):
        user = self.scope.get('user')
        try:
            account = Account.objects.get(id=account_id, user=user)
            account.delete()
        except Transaction.DoesNotExist:
            logging.error(f"Account with ID {account_id} does not exist or does not belong to the user.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while deleting the transaction: {e}")


    @sync_to_async
    def save_transaction(self, account_name, transaction_type, description, amount):
        
        try:
            account = Account.objects.get(name=account_name, user=self.scope.get('user'))
            if transaction_type == 'income':
                amount = Decimal(amount)
                account.amount -= amount 
                account.save()
            else:
                amount = Decimal(amount)
                account.amount += amount 
                account.save()
            Transaction.objects.create(
            user=self.scope.get('user'),
            account=account, 
            transaction_type=transaction_type, 
            description=description,
            amount=amount
        )
        except Account.DoesNotExist:
            logging.error(f"Account with ID {account} does not exist or does not belong to the user.")

    @sync_to_async
    def save_delete_transaction(self, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.delete()
        except Transaction.DoesNotExist:
            logging.error(f"Transaction with ID {transaction_id} does not exist or does not belong to the user.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while deleting the transaction: {e}")

