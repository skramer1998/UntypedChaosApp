from django.test import TestCase
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course


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