from django.test import TestCase, Client
from FSA.accountmodel.account import Account


# Acceptance test classes
class TestUser(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.get('/register/')
        self.c.post('/register/', {'name': 'tyler', 'email': 'x@gmail.com', 'username': 'tdn', 'password': 'password',
                                   'passwordV': 'password', 'phone': '5556969', 'address': '123 lane', 'hours': '12-2',
                                   'groupid': '1'})
        self.c.get('')
        self.c.post('', {'username': 'tdn', 'password': 'password'})
        # creates account and logs into user page

    def test_info(self):
        response = self.c.get('/user/')
        self.assertEqual(response.status_code, 200)
        # we are now logged in on the user page

        self.assertEqual(Account.objects.all().filter(SignInName='tdn').get().userEmail, 'x@gmail.com')
        self.assertEqual(Account.objects.all().filter(SignInName='tdn').get().groupid, 1)
        self.assertEqual(Account.objects.all().filter(SignInName='tdn').get().userPass, 'password')
        # checks data and password are stored properly

    def test_update(self):
        self.c.post('/user/', {'email': 't@gmail.com', 'phone': '5556969', 'address': '567 Street', 'hours': '12-2',
                               'update_account': True})
        self.assertEqual(Account.objects.all().filter(SignInName='tdn').get().userEmail, 't@gmail.com')
        self.assertEqual(Account.objects.all().filter(SignInName='tdn').get().userAddress, '567 Street')
        # checks that update account info works

        self.c.post('/user/', {'oldPass': 'password', 'newPass1': 'yeet', 'newPass2': 'yeet', 'update_password': True})
        self.assertEqual(Account.objects.all().filter(SignInName='tdn').get().userPass, 'yeet')
        # checks that update password works correctly

    def test_links(self):
        response = self.c.get('/registerloggedin/')
        self.assertEqual(response.status_code, 200)
        # we can access register page from user

        self.c.get('/logout/')
        response = self.c.get('')
        self.assertEqual(response.status_code, 200)
        # we can logout from user, brings us back to login page