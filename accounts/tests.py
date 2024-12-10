from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Account

# Account Test case 
class AccountTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        User = get_user_model()
        cls.user = User.objects.create(
            username='TestUser',
            email='test@example.com',
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1000
        )

    # testing account data function
    def test_account_content(self):
        account = Account.objects.get(id=1)

        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.balance, 1000)
        self.assertEqual(str(self.account), self.user.username)
