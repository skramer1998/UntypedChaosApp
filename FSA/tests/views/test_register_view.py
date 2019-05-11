from django.test import TestCase, Client
from FSA.accountmodel.account import Account


# Acceptance test classes
class TestRegister(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

        # create first account supervisor account
        self.client.post('/register/', {'email': 'super@email.com', 'username': 'superuser', 'password': 'superpass',
                                        'passwordV': 'superpass', 'name': 'Supervisor Name', 'phone': '1234567890',
                                        'address': 'Milwaukee Street', 'groupid': '1',
                                        'hours': 'Monday 10:00am-11:00am'})
        # should only be one account in database
        self.assertEqual(Account.objects.all().count(), 1)
        # check to see supervisor was made correctly
        getUser = Account.objects.all().filter(SignInName='superuser', groupid='1')
        getUser = getUser[0]
        getUser = getUser.SignInName
        self.assertEqual(getUser, 'superuser')

        # create another supervisor account but should not go through
        self.client.post('/register/',
                         {'email': 'super@email.com', 'username': 'fakesuperuser', 'password': 'superpass',
                          'passwordV': 'superpass', 'name': 'Supervisor Name', 'phone': '1234567890',
                          'address': 'Milwaukee Street', 'groupid': '1',
                          'hours': 'Monday 10:00am-11:00am'})
        # should only be one account in database
        self.assertEqual(Account.objects.all().count(), 1)
        # should not overwrite original supervisor
        getUser = Account.objects.all().filter(SignInName='superuser', groupid='1')
        getUser = getUser[0]
        getUser = getUser.SignInName
        self.assertEqual(getUser, 'superuser')

        # create admin account with same username as supervisor but should not go through
        self.client.post('/register/',
                         {'email': 'admin@email.com', 'username': 'superuser', 'password': 'superpass',
                          'passwordV': 'superpass', 'name': 'Supervisor Name', 'phone': '1234567890',
                          'address': 'Milwaukee Street', 'groupid': '2',
                          'hours': 'Monday 10:00am-11:00am'})
        # should only be one account in database
        self.assertEqual(Account.objects.all().count(), 1)
        # should not overwrite original supervisor
        getUser = Account.objects.all().filter(SignInName='superuser')
        getUser = getUser[0]
        getUser = getUser.SignInName
        self.assertEqual(getUser, 'superuser')

        # create second account type admin
        self.client.post('/register/', {'email': 'admin@email.com', 'username': 'adminuser', 'password': 'adminpass',
                                        'passwordV': 'adminpass', 'name': 'Admin Name', 'phone': '1234567890',
                                        'address': 'Milwaukee Street', 'groupid': '2',
                                        'hours': 'Monday 10:00am-11:00am'})
        # should be two accounts in database
        self.assertEqual(Account.objects.all().count(), 2)
        # check to see admin was made correctly
        getUser = Account.objects.all().filter(SignInName='adminuser', groupid='2')
        getUser = getUser[0]
        getUser = getUser.SignInName
        self.assertEqual(getUser, 'adminuser')

        # create another admin account but should not go through
        self.client.post('/register/', {'email': 'admin@email.com', 'username': 'fakeadmin', 'password': 'adminpass',
                                        'passwordV': 'adminpass', 'name': 'Admin Name', 'phone': '1234567890',
                                        'address': 'Milwaukee Street', 'groupid': '2',
                                        'hours': 'Monday 10:00am-11:00am'})
        # should be two accounts in database
        self.assertEqual(Account.objects.all().count(), 2)
        # should not overwrite original admin
        getUser = Account.objects.all().filter(SignInName='adminuser', groupid='2')
        getUser = getUser[0]
        getUser = getUser.SignInName
        self.assertEqual(getUser, 'adminuser')
