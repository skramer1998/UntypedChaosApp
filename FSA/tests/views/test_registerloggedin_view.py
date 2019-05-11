from django.test import TestCase, Client
from FSA.accountmodel.account import Account


# Acceptance test classes
class TestRegisterloggedin(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.get('/register/')
        self.c.post('/register/',
                    {'name': 'Phillip', 'email': 'pm@email.com', 'username': 'moss', 'password': 'password',
                     'passwordV': 'password', 'phone': '1234567890', 'address': '123 Sesame Street', 'hours': 'n/a',
                     'groupid': '1'})
        self.c.post('', {'username': 'moss', 'password': 'password'})
        self.c.get('/registerloggedin/')

    def testAdminCreate(self):
        self.c.post('/registerloggedin/', {'name': 'admin', 'email': 'admin@email.com', 'username': 'admin',
                                           'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11',
                                           'groupid': '2'})
        self.assertEqual(Account.objects.all().filter(groupid=2).count(), 1)
        user = Account.objects.all().filter(SignInName='admin')
        user = user[0]
        user = user.SignInName
        self.assertEqual(user, "admin")

    def test_InstructorCreate(self):
        self.c.post('/registerloggedin/',
                    {'name': 'instructor', 'email': 'instructor@email.com', 'username': 'instructor',
                     'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11', 'groupid': '3'})
        self.assertEqual(Account.objects.all().filter(groupid=3).count(), 1)
        user = Account.objects.all().filter(SignInName='instructor')
        user = user[0]
        user = user.SignInName
        self.assertEqual(user, "instructor")

    def test_TACreate(self):
        self.c.post('/registerloggedin/',
                    {'name': 'ta', 'email': 'ta@email.com', 'username': 'ta', 'phone': '0987654321',
                     'address': 'default', 'hours': 'Monday 10-11', 'groupid': '4'})
        self.assertEqual(Account.objects.all().filter(groupid=4).count(), 1)
        user = Account.objects.all().filter(SignInName='ta')
        user = user[0]
        user = user.SignInName
        self.assertEqual(user, "ta")

    def test_failAdminCreateAdmin(self):
        self.c.post('/registerloggedin/', {'name': 'admin', 'email': 'admin@email.com', 'username': 'admin',
                                           'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11',
                                           'groupid': '2'})
        self.c.get('/logout/')
        self.c.post('', {'username': 'admin', 'password': 'admin'})

        self.c.post('/registerloggedin/', {'name': 'fakeadmin', 'email': 'fakeadmin@email.com', 'username': 'fakeadmin',
                                           'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11',
                                           'groupid': '2'})
        self.assertEqual(Account.objects.all().filter(groupid=2).count(), 1)
        user = Account.objects.all().filter(groupid=2)
        user = user[0]
        user = user.SignInName
        self.assertEqual(user, "admin")