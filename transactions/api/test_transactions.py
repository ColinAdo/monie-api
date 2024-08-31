from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import Account
from transactions.models import Transaction
from transactions.api.serializers import TransactionSerializer

# Test transactions api
class AccountApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='TestUser',
            email='TestEmail@test.com'
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1700
        )
        cls.transaction = Transaction.objects.create(
            account=cls.account,
            amount=1400,
            transaction_type='sent'
        )

        cls.airtime = Transaction.objects.create(
            account=cls.account,
            amount=200,
            transaction_type='airtime',
            content='content2',
        )
        cls.received = Transaction.objects.create(
            account=cls.account,
            amount=2000,
            transaction_type='received',
            content='content3',
        )
        cls.withdraw = Transaction.objects.create(
            account=cls.account,
            amount=1000,
            transaction_type='withdraw',
            content='content4',
        )

        cls.access_token = AccessToken.for_user(cls.user)

    # all transactions test
    def test_post_transactions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('transactions-list')
        data = {
            'account': self.account.id,
            'amount': 200,
            'transaction_type': 'withdraw'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 5)

    # test get transaction
    def test_get_transactions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('transactions-list')
        response = self.client.get(url, format='json')

        queryset = Transaction.objects.all()
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 4)

    # test retrieve transaction
    def test_retrieve_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('transactions-detail', kwargs={'pk': self.transaction.id})
        response = self.client.get(url, format='json')

        queryset = Transaction.objects.get(pk=self.transaction.id)
        expected_date = TransactionSerializer(queryset).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertContains(response, self.user.id)

    def test_update_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('transactions-detail', kwargs={'pk': self.transaction.id})
        data = {
            'account': self.account.id,
            'amount': 150,
            'transaction_type': 'sent'
        }
        response = self.client.put(url, data, format='json')

        self.transaction.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.transaction.amount, 150)

    def test_delete_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('transactions-detail', kwargs={'pk': self.transaction.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 3)

    # Sent transaction
    def test_get_sent_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('sent-list')
        response = self.client.get(url, format='json')

        queryset = Transaction.objects.filter(transaction_type='sent')
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)

    # Received transaction
    def test_get_received_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('received-list')
        response = self.client.get(url, format='json')

        queryset = Transaction.objects.filter(transaction_type='received')
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)

    # Withdraw transaction
    def test_get_withdraw_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('withdraw-list')
        response = self.client.get(url, format='json')

        queryset = Transaction.objects.filter(transaction_type='withdraw')
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)

    # Airtime transaction
    def test_get_airtime_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('airtime-list')
        response = self.client.get(url, format='json')

        queryset = Transaction.objects.filter(transaction_type='airtime')
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)
