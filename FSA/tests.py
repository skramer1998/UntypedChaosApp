from django.test import TestCase, Client
from FSA.models import Account
from FSA.models import Course

"""
ACCEPTANCE TESTS ARE AT THE BOTTOM
"""


class TestAccount(TestCase):

    def setUp(self):
        self.t = 4
        self.i = 3
        self.a = 2
        self.s = 1
        # 4 ID's

        self.a1 = Account.create(username="Nate4", name="Nate Z", email="glasses@gmail.com",
                                 phone=1234567890, address="22 Middleton rd", password1="password",
                                 password2="password", id=self.t, hours="10-11")
        self.a2 = Account.create(username="Andres3", name="Andres Z", email="sweatshirt@gmail.com",
                                 phone=2121212121, address="34 Giannis rd", password1="password",
                                 password2="password", id=self.i, hours="11-12")
        self.a3 = Account.create(username="Sean2", name="Sean Z", email="tshirt@gmail.com",
                                 phone=4145554444, address="13 Brogdon ave", password1="password",
                                 password2="password", id=self.a, hours="12-1")
        self.a4 = Account.create(username="Tyler1", name="Tyler Z", email="jersey@gmail.com",
                                 phone=4207106969, address="11 Bledsoe ct", password1="password",
                                 password2="password", id=self.s, hours="1-2")
        # creates 4 accounts with each level of ID

        # Create accounts with blank fields
        self.a5 = Account.create(username="skramer", name="Sean Kramer", email="",
                                 phone="", address="", password1="abc123", password2="abc123",
                                 id=self.i, hours="")

    def test_create(self):
        self.assertEqual(Account.create(username="Nate5", name="Nate Z", email="glasses@gmail.com",
                                        phone=1234567890, address="22 Middleton rd", password1="",
                                        password2="", id=self.t, hours="10-11"),
                         "password cannot be blank")
        # blank password

        self.assertEqual(Account.create(username="Nate4", name="Nate Z", email="glasses@gmail.com",
                                        phone=1234567890, address="22 Middleton rd", password1="",
                                        password2="password2", id=self.t, hours="10-11"),
                         "passwords don't match, couldn't create account")
        # passwords do not match

        # Check blank fields work
        self.assertEqual(self.a5.SignInName, "skramer")
        self.assertEqual(self.a5.userPass, "abc123")
        self.assertEqual(self.a5.userName, "Sean Kramer")
        self.assertEqual(self.a5.userEmail, "")
        self.assertEqual(self.a5.userPhone, "")
        self.assertEqual(self.a5.userAddress, "")
        self.assertEqual(self.a5.groupid, self.i)
        self.assertEqual(self.a5.userHours, "")

        self.assertEqual(self.a2.SignInName, "Andres3")
        self.assertEqual(self.a2.userName, "Andres Z")
        self.assertEqual(self.a2.userEmail, "sweatshirt@gmail.com")
        self.assertEqual(self.a2.userPhone, 2121212121)
        self.assertEqual(self.a2.userAddress, "34 Giannis rd")
        self.assertEqual(self.a2.userHours, "11-12")
        # Cannot check password values from account object
        # self.assertEqual(self.a2.password1, "password")
        # self.assertEqual(self.a2.password2, "password")
        self.assertEqual(self.a2.groupid, self.i)
        # checks Account a2 was created properly

        self.assertNotEqual(self.a2.SignInName, "")
        self.assertNotEqual(self.a2.userName, "")
        self.assertNotEqual(self.a2.userEmail, "")
        self.assertNotEqual(self.a2.userPhone, "")
        self.assertNotEqual(self.a2.userAddress, "")
        self.assertNotEqual(self.a2.userHours, "")
        # self.assertNotEqual(self.a2.password1, "")
        # self.assertNotEqual(self.a2.password2, "")
        self.assertNotEqual(self.a2.groupid, "")
        # checks not blank

    def test_getid(self):
        # Test if userID retrieval works
        self.assertEqual(self.a1.getid(self.a1), self.t)

    def test_updateUser(self):
        # Test updating all params
        self.assertEqual(
            Account.updateUser(self.a1, email="uwm@uwm.edu", phone="2624929332", address="wherever dr", hours="12-5"),
            "Account information updated.")
        self.assertEqual(self.a1.userEmail, "uwm@uwm.edu")
        self.assertEqual(self.a1.userPhone, "2624929332")
        self.assertEqual(self.a1.userAddress, "wherever dr")
        self.assertEqual(self.a1.userHours, "12-5")

        # Test updating three params
        self.assertEqual(
            Account.updateUser(self.a1, email="uwm2@uwm.edu", phone="4144929332", address="whoever dr", hours=""),
            "Account information updated.")
        self.assertEqual(self.a1.userEmail, "uwm2@uwm.edu")
        self.assertEqual(self.a1.userPhone, "4144929332")
        self.assertEqual(self.a1.userAddress, "whoever dr")
        self.assertEqual(self.a1.userHours, "12-5")

        # Test updating two params
        self.assertEqual(Account.updateUser(self.a1, email="uwm3@uwm.edu", phone="5154929332", address="", hours=""),
                         "Account information updated.")
        self.assertEqual(self.a1.userEmail, "uwm3@uwm.edu")
        self.assertEqual(self.a1.userPhone, "5154929332")
        self.assertEqual(self.a1.userAddress, "whoever dr")
        self.assertEqual(self.a1.userHours, "12-5")

        # Test updating one param
        self.assertEqual(Account.updateUser(self.a1, email="uwm3@uwm.edu", phone="", address="", hours=""),
                         "Account information updated.")
        self.assertEqual(self.a1.userEmail, "uwm3@uwm.edu")
        self.assertEqual(self.a1.userPhone, "5154929332")
        self.assertEqual(self.a1.userAddress, "whoever dr")
        self.assertEqual(self.a1.userHours, "12-5")

        # Test updating no params
        self.assertEqual(Account.updateUser(self.a1, email="", phone="", address="", hours=""),
                         "Account information updated.")
        self.assertEqual(self.a1.userEmail, "uwm3@uwm.edu")
        self.assertEqual(self.a1.userPhone, "5154929332")
        self.assertEqual(self.a1.userAddress, "whoever dr")
        self.assertEqual(self.a1.userHours, "12-5")

    def test_updatePass(self):
        # Test updating password correctly
        self.assertEqual(Account.updatePass(self.a1, oldPass="password", newPass1="abc123", newPass2="abc123"),
                         "Password updated successfully.")
        self.assertEqual(self.a1.userPass, "abc123")

        # Test updating password incorrectly, bad old pass
        self.assertEqual(Account.updatePass(self.a1, oldPass="wordpass", newPass1="abc1234", newPass2="abc1234"),
                         "Old password is not correct.")
        self.assertEqual(self.a1.userPass, "abc123")

        # Test updating password incorrectly, mismatch new passes
        self.assertEqual(Account.updatePass(self.a1, oldPass="abc123", newPass1="abc1234", newPass2="cba4321"),
                         "New passwords do not match.")
        self.assertEqual(self.a1.userPass, "abc123")


class TestCourse(TestCase):

    def setUp(self):
        self.a1 = Account.create(username="Nate4", name="Nate Z", email="glasses@gmail.com",
                                 phone=1234567890, address="22 Middleton rd", password1="password",
                                 password2="password", id=4, hours="10-11")
        self.a2 = Account.create(username="Andres3", name="Andres Z", email="sweatshirt@gmail.com",
                                 phone=2121212121, address="34 Giannis rd", password1="password",
                                 password2="password", id=3, hours="11-12")
        self.a3 = Account.create(username="Sean2", name="Sean Z", email="tshirt@gmail.com",
                                 phone=4145554444, address="13 Brogdon ave", password1="password",
                                 password2="password", id=2, hours="12-1")
        self.a4 = Account.create(username="Tyler1", name="Tyler Z", email="jersey@gmail.com",
                                 phone=4207106969, address="11 Bledsoe ct", password1="password",
                                 password2="password", id=1, hours="1-2")

        # create 4 accounts for assign functions

        self.c1 = Course.create("History of Math", 200, "EMS", "MWF", "01:00 - 01:50", "FALL", "Andres3", "Nate4")
        self.c2 = Course.create("History of Baths", 500, "EBS", "F", "20:00 - 20:50", "FALL", "Andres3", "Nate4")
        # create our test courses

    def testCreate(self):
        self.assertEqual(self.c1.name, "History of Math")
        self.assertEqual(self.c1.number, 200)
        self.assertEqual(self.c1.place, "EMS")
        self.assertEqual(self.c1.days, "MWF")
        self.assertEqual(self.c1.time, "01:00 - 01:50")
        self.assertEqual(self.c1.semester, "FALL")
        self.assertEqual(self.c1.professor.SignInName, "Andres3")
        self.assertEqual(self.c1.ta.SignInName, "Nate4")
        # checks course c1 was created properly

        self.assertEqual(
            Course.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                          self.c1.professor, self.c1.ta), "That course already exists.")
        # should return this if already exists

    def testSearch(self):
        self.assertTrue(self.c1.search("History of Baths"))
        # should be true

        self.assertFalse(self.c2.search("History"))
        self.assertFalse(self.c2.search("Chinese Horse Energy"))
        # should both be false.

    def test_assignin(self):
        self.assertEqual(Course.assignin("History of Math", self.a4.SignInName),
                         "Administrators and Supervisors cannot be assigned to a course.")
        self.assertEqual(Course.assignin("History of Math", self.a3.SignInName),
                         "Administrators and Supervisors cannot be assigned to a course.")
        # attempts to set a supervisor/admin to a course

        self.assertEqual(Course.assignin("Clown Class", self.a1.SignInName), "There is no course named Clown Class")
        self.assertEqual(Course.assignin("History of Math", "Rick Flair"), "There is no account named Rick Flair")
        # checks parameters exist

    def test_assignta(self):
        self.assertEqual(Course.assignta("History of Math", self.a2),
                         "Administrators and Supervisors cannot be assigned to a course.")
        self.assertEqual(Course.assignta("History of Math", self.a2),
                         "Administrators and Supervisors cannot be assigned to a course.")
        self.assertEqual(Course.assignta("History of Math", self.a2),
                         "Administrators and Supervisors cannot be assigned to a course.")
        # attempts setting non TA to a lab

        self.assertEqual(Course.assignta("Clown Class", self.a1.userName), "There is no course named Clown Class")
        self.assertEqual(Course.assignta("History of Math", "Rick Flair"), "There is no account named Rick Flair")
        # checks parameters exist

    def test__str__(self):
        self.assertEqual(self.c2.__str__(), "History of Baths 500 EBS F 20:00 - 20:50 FALL Andres3 Nate4")
        # asserts toStr has correct format


# Acceptance test class
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

    def test_not_enough_information(self):
        # go to post with all empty fields
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': '', 'name': '',
                                        'phone': '', 'address': '', 'groupid': '', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only name in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': '',
                                        'name': 'onlyName', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only username in post
        self.client.post('/register/', {'email': '', 'username': 'onlyUsername', 'password': '', 'passwordV': '',
                                        'name': '', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only password in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': 'onlyPassword', 'passwordV': '',
                                        'name': '', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only passwordV in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': 'onlyPasswordV',
                                        'name': '', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only passwordV in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': 'onlyPasswordV',
                                        'name': '', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only email in post
        self.client.post('/register/', {'email': 'email@uwm.edu', 'username': '', 'password': '', 'passwordV': '',
                                        'name': '', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only phone in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': '',
                                        'name': '', 'phone': '1234567890', 'address': '', 'groupid': '1', 'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only address in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': '',
                                        'name': '', 'phone': '', 'address': 'Milwaukee Somewhere', 'groupid': '1',
                                        'hours': ''})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

        # only hours in post
        self.client.post('/register/', {'email': '', 'username': '', 'password': '', 'passwordV': '',
                                        'name': '', 'phone': '', 'address': '', 'groupid': '1', 'hours': 'Monday'})
        # nothing should be created
        self.assertEqual(Account.objects.all().count(), 0)

    def test_barely_enough_information(self):
        # only needs username, password, passwordV, name, groupid
        self.client.post('/register/', {'email': '', 'username': 'NeedS', 'password': 'match', 'passwordV': 'match',
                                        'name': 'Need', 'phone': '', 'address': '', 'groupid': '1', 'hours': ''})
        # one account in database
        self.assertEqual(Account.objects.all().count(), 1)

        # only needs username, password, passwordV, name, groupid
        self.client.post('/register/', {'email': '', 'username': 'NeedA', 'password': 'match', 'passwordV': 'match',
                                        'name': 'Need', 'phone': '', 'address': '', 'groupid': '2', 'hours': ''})
        # two accounts in database
        self.assertEqual(Account.objects.all().count(), 2)


# Acceptance test class
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


class LoginTest(TestCase):  # Acceptance tests for our login page

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_setup(self):
        # Issue a GET request for the main page, which is login
        response = self.client.get('/')
        # check that it's ok
        self.assertEqual(response.status_code, 200)

    def test_loginRedirectResponses(self):
        # setup
        Account.create(username="Nate5", name="Nate Z", email="glasses@gmail.com",
                       phone=1234567890, address="22 Middleton rd", password1="password",
                       password2="password", id=1, hours="10-11")
        # pass along existing credentials from setup
        response = self.client.post('/', {'username': 'Nate5', 'password': 'password'})
        # see if those are good, redirect to main page if all is well
        self.assertEqual(response.status_code, 302)

    def test_loginFailRedirectResponse(self):
        # pass along bad credentials
        response = self.client.post('/', {'username': 'NotGood', 'password': 'NotGood'})
        # see if it rejects those, which will keep them  ar the login page
        self.assertEqual(response.status_code, 200)

    def test_loginFailedNoCredentials(self):
        # pass along empty
        response = self.client.post('/', {'username': '', 'password': ''})
        # keep user at login page
        self.assertEqual(response.status_code, 200)
