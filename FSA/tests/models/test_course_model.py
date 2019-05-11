from django.test import TestCase
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section, Lab


class TestCourse(TestCase):

    def setUp(self):
        # create 4 accounts for assign functions
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

        # Create Courses
        self.c1 = Course.create("History of Math", 200, "FALL")
        self.c2 = Course.create("History of Baths", 500, "FALL")

        # Create Sections
        Section.create(self.c1.name, 401, self.a3)
        self.s1 = Section.get(self.c1.name, 401)
        Section.create(self.c1.name, 402, self.a3)
        self.s2 = Section.get(self.c1.name, 402)
        Section.create(self.c2.name, 501, self.a3)
        self.s3 = Section.get(self.c2.name, 501)
        Section.create(self.c2.name, 502, self.a3)
        self.s4 = Section.get(self.c2.name, 502)

        # Create Labs
        Lab.create(self.c1.name, self.s1.number, 801, self.a4)
        self.l1 = Lab.get(self.c1.name, self.s1.number, 801)
        Lab.create(self.c2.name, self.s3.number, 901, self.a4)
        self.l2 = Lab.get(self.c2.name, self.s3.number, 901)

    def testCreate(self):
        # Check Course Creation
        self.assertEqual(self.c1.name, "History of Math")
        self.assertEqual(self.c1.number, 200)
        self.assertEqual(self.c1.semester, "FALL")

        self.assertEqual(self.c2.name, "History of Baths")
        self.assertEqual(self.c2.number, 500)
        self.assertEqual(self.c2.semester, "FALL")

        # Check Section Creation
        self.assertEqual(self.s1.parentCourse, "History of Math")
        self.assertEqual(self.s1.number, 401)
        self.assertEqual(self.s1.place, "")
        self.assertEqual(self.s1.days, "")
        self.assertEqual(self.s1.time, "")
        self.assertEqual(self.s1.instructor, self.a3)

        self.assertEqual(self.s2.parentCourse, "History of Math")
        self.assertEqual(self.s2.number, 402)
        self.assertEqual(self.s2.place, "")
        self.assertEqual(self.s2.days, "")
        self.assertEqual(self.s2.time, "")
        self.assertEqual(self.s2.instructor, self.a3)

        self.assertEqual(self.s3.parentCourse, "History of Baths")
        self.assertEqual(self.s3.number, 501)
        self.assertEqual(self.s3.place, "")
        self.assertEqual(self.s3.days, "")
        self.assertEqual(self.s3.time, "")
        self.assertEqual(self.s3.instructor, self.a3)

        self.assertEqual(self.s4.parentCourse, "History of Baths")
        self.assertEqual(self.s4.number, 502)
        self.assertEqual(self.s4.place, "")
        self.assertEqual(self.s4.days, "")
        self.assertEqual(self.s4.time, "")
        self.assertEqual(self.s4.instructor, self.a3)

        # Check Lab Creation
        self.assertEqual(self.l1.parentCourse, "401")
        self.assertEqual(self.l1.number, 801)
        self.assertEqual(self.l1.place, "")
        self.assertEqual(self.l1.days, "")
        self.assertEqual(self.l1.time, "")
        self.assertEqual(self.l1.ta, self.a4)

        self.assertEqual(self.l2.parentCourse, "501")
        self.assertEqual(self.l2.number, 901)
        self.assertEqual(self.l2.place, "")
        self.assertEqual(self.l2.days, "")
        self.assertEqual(self.l2.time, "")
        self.assertEqual(self.l2.ta, self.a4)

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
        self.assertEqual(self.c2.__str__(), "History of Baths 500 FALL")
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