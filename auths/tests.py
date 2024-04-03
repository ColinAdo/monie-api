from django.test import TestCase
from django.contrib.auth import get_user_model


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
