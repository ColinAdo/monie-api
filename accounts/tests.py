from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Account, Transaction, Notification


class AccountTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        User = get_user_model()
        cls.user = User.objects.create(
            username="TestUser",
            email="test@example.com",
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1000
        )

    def test_account_content(self):
        account = Account.objects.get(id=1)

        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.balance, 1000)

    def test_return_string(self):
        self.assertEqual(str(self.account), self.user.username)


class TransactionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username="TestUser",
            email="test@example.com",
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1000
        )

        cls.transaction = Transaction.objects.create(
            account=cls.account,
            amount=1000,
            transaction_type="sent"
        )

    def test_transaction_content(self):

        transaction = Transaction.objects.get(id=1)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.amount, 1000)

    def test_return_string(self):
        self.assertEqual(str(self.transaction), "sent")


class NotificationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username="TestUser",
            email="test@example.com",
        )

        cls.account = Account.objects.create(
            user=cls.user,
            balance=1000
        )

        cls.transaction = Transaction.objects.create(
            account=cls.account,
            amount=1000,
            transaction_type="sent"
        )

        cls.notification = Notification.objects.create(
            transaction=cls.transaction,
            content="You have received ksh 1000,000",
        )

    def test_notification_content(self):

        notification = Notification.objects.get(id=1)

        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(notification.transaction, self.transaction)
        self.assertEqual(notification.content, "You have received ksh 1000,000")

    def test_return_string(self):
        self.assertEqual(str(self.notification), "You have received ks...")
