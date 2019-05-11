from django.test import TestCase, Client
from FSA.accountmodel.account import Account


class EditUserTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.c.get('/register/')
        self.c.post('/register/',
                    {'name': 'Phillip', 'email': 'pm@email.com', 'username': 'moss', 'password': 'password',
                     'passwordV': 'password', 'phone': '1234567890', 'address': '123 Sesame Street', 'hours': 'n/a',
                     'groupid': '1'})
        self.c.post('', {'username': 'moss', 'password': 'password'})
        self.c.get('/registerloggedin/')

        self.c.post('/registerloggedin/', {'name': 'admin', 'email': 'admin@email.com', 'username': 'admin',
                                           'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11',
                                           'groupid': '2'})

        self.c.post('/registerloggedin/',
                    {'name': 'instructor', 'email': 'instructor@email.com', 'username': 'instructor',
                     'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11', 'groupid': '3'})

        self.c.post('/registerloggedin/',
                    {'name': 'ta', 'email': 'ta@email.com', 'username': 'ta', 'phone': '0987654321',
                     'address': 'default', 'hours': 'Monday 10-11', 'groupid': '4'})
        self.c.get('/user/')

    def test_edituseradmin(self):
        """ edit admin """
        self.c.get('/edituser/?info=admin')
        self.c.post('/edituser/?info=admin', {'email': 'and@and.com', 'phone': '1234567890', 'address': 'milwaukee',
                                              'hours': '10am-11am', 'currentUser': 'admin',
                                              'update_account': 'update_account'})

        user: Account = Account.objects.all().filter(SignInName='admin').first()
        self.assertEqual(user.userEmail, 'and@and.com')
        self.assertEqual(user.userPhone, '1234567890')
        self.assertEqual(user.userAddress, 'milwaukee')
        self.assertEqual(user.userHours, '10am-11am')

    def test_edituserinstructor(self):
        """ edit instructor """
        self.c.get('/edituser/?info=instructor')
        self.c.post('/edituser/?info=instructor',
                    {'email': 'and@and.com', 'phone': '1234567890', 'address': 'milwaukee',
                     'hours': '10am-11am', 'currentUser': 'instructor',
                     'update_account': 'update_account'})

        user: Account = Account.objects.all().filter(SignInName='instructor').first()
        self.assertEqual(user.userEmail, 'and@and.com')
        self.assertEqual(user.userPhone, '1234567890')
        self.assertEqual(user.userAddress, 'milwaukee')
        self.assertEqual(user.userHours, '10am-11am')

    def test_edituserta(self):
        """ edit ta """
        self.c.get('/edituser/?info=instructor')
        self.c.post('/edituser/?info=instructor',
                    {'email': 'and@and.com', 'phone': '1234567890', 'address': 'milwaukee',
                     'hours': '10am-11am', 'currentUser': 'instructor',
                     'update_account': 'update_account'})

        user: Account = Account.objects.all().filter(SignInName='instructor').first()
        self.assertEqual(user.userEmail, 'and@and.com')
        self.assertEqual(user.userPhone, '1234567890')
        self.assertEqual(user.userAddress, 'milwaukee')
        self.assertEqual(user.userHours, '10am-11am')
