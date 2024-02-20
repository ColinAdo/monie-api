from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import Account
from accounts.api.serializers import AccountSerializer


class AccountTestCase(APITestCase):
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

    def test_create_account_api(self):
        url = reverse('accounts')
        data = {
            "user": self.user.id,
            "balance": 200
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_list_accounts_api(self):
        url = reverse('accounts')
        response = self.client.get(url, format='json')

        queryset = Account.objects.all()
        expected_date = AccountSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)

    def test_account_detail_api(self):
        url = reverse('account-detail', kwargs={'pk': self.account.id})
        response = self.client.get(url, format='json')

        queryset = Account.objects.get(pk=self.account.id)
        expected_date = AccountSerializer(queryset).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertContains(response, self.user.id)
