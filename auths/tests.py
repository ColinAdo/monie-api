from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from core.authentication import CustomJWTAuthentication

# User test case
class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        User = get_user_model()
        cls.user = User.objects.create(
            username="TestUser",
            email="test@example.com",
        )

    def test_user_contents(self):
        self.assertEqual(self.user.username, 'TestUser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(str(self.user), 'TestUser')

# Custom jwt authentication test case
class CustomJWTAuthenticationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.auth = CustomJWTAuthentication()

        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

        cls.access_token = AccessToken.for_user(cls.user)

    def test_authenticate_no_token(self):
        request = self.factory.get('/')

        request = self.auth.authenticate(request)

        self.assertIsNone(request)

    def test_authenticate_invalid_token(self):
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer invalidtoken'
        
        result = self.auth.authenticate(request)
        
        self.assertIsNone(result)