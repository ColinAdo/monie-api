from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import Account
from accounts.api.serializers import AccountSerializer
from accounts.api.permissions import IsOwnerOrReadOnly

# account test case
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
        cls.access_token = AccessToken.for_user(cls.user)

    def test_post_account(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('accounts-list')
        data = {
            "user": self.user.id,
            "balance": 200
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_get_accounts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('accounts-list')
        response = self.client.get(url, format='json')

        queryset = Account.objects.all()
        expected_date = AccountSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_accounts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('accounts-detail', kwargs={'pk': self.account.id})
        response = self.client.get(url, format='json')

        queryset = Account.objects.get(pk=self.account.id)
        expected_date = AccountSerializer(queryset).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_date)
        self.assertContains(response, self.user.id)

# Is owner or read only test case
class IsOwnerOrReadOnlyTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com'
        )
        cls.other_user = User.objects.create(
            username='otheruser',
            email='otheruser@example.com'
        )
        cls.account = Account.objects.create(
            user=cls.user,
            balance=120000
        )
        cls.permission = IsOwnerOrReadOnly()
        cls.view = APIView()
        cls.factory = APIRequestFactory()


    def test_safe_method_permission(self):
        request = self.factory.get('/')
        request.user = self.user

        self.assertTrue(self.permission.has_object_permission(request, self.view, self.account))

    def test_unsafe_method_permission_owner(self):
        request = self.factory.post('/')
        request.user = self.user

        self.assertTrue(self.permission.has_object_permission(request, self.view, self.account))

    def test_unsafe_method_permission_non_owner(self):
        request = self.factory.post('/')
        request.user = self.other_user

        self.assertFalse(self.permission.has_object_permission(request, self.view, self.account))