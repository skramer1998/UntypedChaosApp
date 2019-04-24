from django.test import TestCase, Client
from FSA.models import Account
from FSA.models import Course


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

    #def test_updateUser(self):
        #self.assertEqual(Account.updateUser(self.a1, "uwm@uwm.edu", ""))

    '''
    def test_editSelf(self):
        # self.assertEqual(self.a1.editSelf(), "Incorrect parameters given.")
        # self.assertEqual(self.a1.editSelf("Howdy yall, I'm Towly!"), "Incorrect parameters given.")
        # self.assertEqual(self.a1.editSelf(SignInName="NateDog"), "Incorrect parameters given.")
        # bad parameters for editSelf, should only return the appropriate string

        self.assertEqual(self.a1.editSelf(username="NateDog", name="Nate Y", email="x@gmail.com",
                                          phone=1010101010, address="The Trap", password1="code",
                                          password2="binary", id=self.i),
                         "passwords don't match, couldn't create account")
        self.assertEqual(self.a1.editSelf(username="NateDog", name="Nate Y", email="x@gmail.com",
                                          phone=1010101010, address="The Trap", password1="",
                                          password2="", id=self.i), "password cannot be blank")
        # invalid passwords

        self.a1.editSelf(username="NateDog", name="Nate Y", email="x@gmail.com",
                         phone=1010101010, address="The Trap", password1="code",
                         password2="code", id=self.i)
        self.assertEqual(self.a1.user.username, "NateDog")
        self.assertEqual(self.a1.user.first_name, "Nate")
        self.assertEqual(self.a1.user.last_name, "Y")
        self.assertEqual(self.a1.user.email, "Nate")
        self.assertEqual(self.a1.userPhone, "1010101010")
        self.assertEqual(self.a1.userAddress, "The Trap")
        self.assertEqual(self.a1.user.password, "code")
        self.assertEqual(self.a1.user.id, self.i)
        # checks if editSelf worked correctly with correct parameters
        pass
    '''

    """    
    def test_editOther(self):
        self.assertFalse(
            self.a1.editOther(self.a1.user, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertFalse(
            self.a1.editOther(self.a1.user, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertTrue(
            self.a1.editOther(self.a1.user, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertTrue(
            self.a1.editOther(self.a1.user, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010))
        self.a1.editSelf("Nate", self.T, "glasses@gmail.com", "22 Middleton Rd", 1234567890)
        # checks only accounts with proper ID can edit other accounts

        self.assertFalse(self.a4.editOther(self.a1))
        self.assertFalse(self.a4.editOther(self.a1, "Howdy yall, I'm Towly!"))
        self.assertFalse(self.a4.editOther(self.a1, 'a', self.I, "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertFalse(
            self.a4.editOther(self.a1, "NateDog", "iNstRectAr", "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", self.I, "Natedog@gmail.com", 42, 1010101010))
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", self.I, "NAT@", "The Trap House", 1010101010))
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1))
        # returns false for bad parameters given

        self.a4.editOther(self.a1, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010)
        self.assertEqual(self.a1.user.username, "NateDog")
        self.assertEqual(self.a1.user.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userName, "NateDog")
        self.assertEqual(self.a1.SignInName, self.I)
        self.assertEqual(self.a1.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userPhone, 1010101010)
        self.assertEqual(self.a1.userAddress, "The Trap House")
        self.a1.editSelf("Nate", self.T, "glasses@gmail.com", "22 Middleton Rd", 1234567890)
        # checks edit other successfully edits user info with correct parameters
        pass

    def test_checkRole(self):
        self.assertTrue(self.a1.is_TA() | self.a1.is_Instructor() | self.a1.is_Admin() | self.a1.is_Supervisor())
        self.assertFalse(self.a1.is_TA() & self.a1.is_Instructor())
        self.assertFalse(self.a1.is_TA() & self.a1.is_Admin())
        self.assertFalse(self.a1.is_TA() & self.a1.is_Supervisor())
        self.assertFalse(self.a1.is_Instructor() & self.a1.is_Admin())
        self.assertFalse(self.a1.is_Instructor() & self.a1.is_Supervisor())
        self.assertFalse(self.a1.is_Admin() & self.a1.is_Supervisor())
        # makes ure user has an ID, and that it does not have more than 1 ID.

        self.assertFalse(self.a1.invalidatePassword(self.a1.user))
        self.assertFalse(self.a2.invalidatePassword(self.a1.user))
        self.assertTrue(self.a3.invalidatePassword(self.a1.user))
        self.assertTrue(self.a4.invalidatePassword(self.a1.user))
        # checks only accounts with proper ID can invalidate passwords

        self.assertFalse(self.a1.createCourse())
        self.assertFalse(self.a2.createCourse())
        self.assertTrue(self.a3.createCourse())
        self.assertTrue(self.a4.createCourse())
        # checks only accounts with proper ID can create courses
        pass
    """


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

    """
    def testSet(self):
        self.c2.setname("Shower Physics")
        self.c2.setnumber(100)
        self.c2.setplace("Physics Building")
        self.c2.setdays("MW")
        self.c2.settime("12:00 - 12:50")
        self.c2.setsemester("SPRING")
        self.c2.setprofessor("GLOCK")
        self.c2.setta("PING")
        # sets new values

        self.assertEqual(self.c2.name, "Shower Physics")
        self.assertEqual(self.c2.number, 100)
        self.assertEqual(self.c2.place, "Physics Building")
        self.assertEqual(self.c2.days, "MW")
        self.assertEqual(self.c2.time, "12:00 - 12:50")
        self.assertEqual(self.c2.semester, "SPRING")
        self.assertEqual(self.c2.professor, "GLOCK")
        self.assertEqual(self.c2.ta, "PING")
        # checks correctly set

        self.assertFalse(self.c2.setname())
        self.assertFalse(self.c2.setnumber())
        self.assertFalse(self.c2.setplace())
        self.assertFalse(self.c2.setdays())
        self.assertFalse(self.c2.settime())
        self.assertFalse(self.c2.setsemester())
        self.assertFalse(self.c2.setprofessor())
        self.assertFalse(self.c2.setta())
        # checks empty set

        self.assertFalse(self.c2.setname(12))
        self.assertFalse(self.c2.setnumber("hi"))
        self.assertFalse(self.c2.setplace(12))
        self.assertFalse(self.c2.setdays(12))
        self.assertFalse(self.c2.settime(12))
        self.assertFalse(self.c2.setsemester(12))
        self.assertFalse(self.c2.setprofessor(12))
        self.assertFalse(self.c2.setta(12))
        # checks incorrectly set

        self.assertTrue(self.c2.search("Shower Physics"))
        self.assertFalse(self.c2.search("History of Baths"))
        # checks updated names in search
        pass
    """


class TestUser(TestCase):
    def setUp(self):
        self.c = Client()

    def test_info(self):
        self.c.get('/register/')
        self.c.post('/register/', {'name': 'tyler', 'email': 'x@gmail.com', 'username': 'tdn', 'password': 'password',
                                   'passwordV': 'password', 'phone': '5556969', 'address': '123 lane', 'hours': '12-2',
                                   'groupid': '1'})

        response = self.c.get('')
        self.assertEqual(response.status_code, 200)
        self.c.post('', {'username': 'tdn', 'password': 'password'})

        response = self.c.get('/user/')
        self.assertEqual(response.status_code, 200)

