from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import Account, Transaction
from accounts.api.serializers import AccountSerializer, TransactionSerializer


class AccountApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username="TestUser",
            email="TestEmail@test.com",
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1700
        )

    def test_post_account(self):
        url = reverse('accounts-list')
        data = {
            "user": self.user.id,
            "balance": 200
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_get_accounts(self):
        url = reverse('accounts-list')
        response = self.client.get(url, format='json')

        queryset = Account.objects.all()
        expected_date = AccountSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)

    def test_retrieve_accounts(self):
        url = reverse('accounts-detail', kwargs={'pk': self.account.id})
        response = self.client.get(url, format='json')

        queryset = Account.objects.get(pk=self.account.id)
        expected_date = AccountSerializer(queryset).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertContains(response, self.user.id)


class TransactionApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username="TestUser",
            email="TestEmail@test.com",
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1700
        )
        cls.transaction1 = Transaction.objects.create(
            account=cls.account,
            amount=1700,
            transaction_type="sent",
            content="content1",
        )
        cls.transaction2 = Transaction.objects.create(
            account=cls.account,
            amount=200,
            transaction_type="airtime",
            content="content2",
        )
        cls.transaction3 = Transaction.objects.create(
            account=cls.account,
            amount=2000,
            transaction_type="received",
            content="content3",
        )
        cls.transaction4 = Transaction.objects.create(
            account=cls.account,
            amount=1000,
            transaction_type="withdraw",
            content="content4",
        )
        cls.transaction5 = Transaction.objects.create(
            account=cls.account,
            amount=1000,
            transaction_type="sent",
            content="content5",
        )

    def test_post_transaction(self):
        url = reverse("transactions-list")
        data = {
            "account": self.account.id,
            "amount": 1000,
            "transaction_type": "withdraw",
            "content": "content5",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 6)

    def test_get_transactions(self):
        url = reverse('transactions-list')
        response = self.client.get(url, format="json")

        queryset = Transaction.objects.all()
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data, expected_date)
        self.assertContains(response, self.account.id)

    def test_retrieve_transactions(self):
        url = reverse("transactions-detail",
                      kwargs={'pk': self.transaction1.id})
        response = self.client.get(url, format="json")

        obj = Transaction.objects.get(id=self.transaction1.id)
        expected_date = TransactionSerializer(obj).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertContains(response, "content1")

    def test_get_sent_transaction(self):
        url = reverse("sent")
        response = self.client.get(url, format="json")

        queryset = Transaction.objects.filter(transaction_type="sent")
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 2)

    def test_get_received_transaction(self):
        url = reverse("received")
        response = self.client.get(url, format="json")

        queryset = Transaction.objects.filter(transaction_type="received")
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)

    def test_get_withdraw_transaction(self):
        url = reverse("withdraw")
        response = self.client.get(url, format="json")

        queryset = Transaction.objects.filter(transaction_type="withdraw")
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)

    def test_get_withdraw_transaction(self):
        url = reverse("airtime")
        response = self.client.get(url, format="json")

        queryset = Transaction.objects.filter(transaction_type="airtime")
        expected_date = TransactionSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)
