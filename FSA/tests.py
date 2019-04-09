from django.test import TestCase
from FSA.models import Account
from FSA.models import Course


class TestAccount(TestCase):

    def setUp(self):
        self.t = 4
        self.i = 3
        self.a = 2
        self.s = 1
        # 4 ID's

        self.a1 = Account.objects.create(userid = "Nate4", username = "Nate Z", email = "glasses@gmail.com",
                                         phone=1234567890, address = "22 Middleton rd", password1 = "password",
                                         password2 = "password", groupid = self.t)
        self.a2 = Account.objects.create(userid="Andres3", username="Andres Z", email="sweatshirt@gmail.com",
                                         phone=2121212121, address="34 Giannis rd", password1="password",
                                         password2="password", groupid=self.i)
        self.a3 = Account.objects.create(userid="Sean2", username="Sean Z", email="tshirt@gmail.com",
                                         phone=4145554444, address="13 Brogdon ave", password1="password",
                                         password2="password", groupid=self.a)
        self.a4 = Account.objects.create(userid="Tyler1", username="Tyler Z", email="jersey@gmail.com",
                                         phone=4207106969, address="11 Bledsoe ct", password1="password",
                                         password2="password", groupid=self.s)
        # creates 4 accounts with each level of ID

    def test_create(self):
        self.assertEqual(Account.objects.create(userid = "Nate4", username = "Nate Z", email = "glasses@gmail.com",
                                                phone=1234567890, address = "22 Middleton rd", password1 = "",
                                                password2 = "", groupid = self.t),
                                                "passwords don't match, couldn't create account")
        # blank password

        self.assertEqual(Account.objects.create(userid="Nate4", username="Nate Z", email="glasses@gmail.com",
                                                phone=1234567890, address="22 Middleton rd", password1="",
                                                password2="password2", groupid=self.t),
                                                "passwords don't match, couldn't create account")
        # passwords do not match

        self.assertEqual(self.a2.userid, "Andres3")
        self.assertEqual(self.a2.username, "Andres Z")
        self.assertEqual(self.a2.email, "sweatshirt@gmail.com")
        self.assertEqual(self.a2.phone,2121212121)
        self.assertEqual(self.a2.address, "34 Giannis rd")
        self.assertEqual(self.a2.password1, "password")
        self.assertEqual(self.a2.password2, "password")
        self.assertEqual(self.a2.groupid, self.i)
        # checks Account a2 was created properly

        self.assertNotEqual(self.a2.userid, "")
        self.assertNotEqual(self.a2.username, "")
        self.assertNotEqual(self.a2.email, "")
        self.assertNotEqual(self.a2.phone, "")
        self.assertNotEqual(self.a2.address, "")
        self.assertNotEqual(self.a2.password1, "")
        self.assertNotEqual(self.a2.password2, "")
        self.assertNotEqual(self.a2.groupid, "")
        # checks not blank

    def test_editSelf(self):
        self.assertFalse(self.a1.editSelf())
        self.assertFalse(self.a1.editSelf("Howdy yall, I'm Towly!"))
        self.assertFalse(self.a1.editSelf('a', self.I, "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertFalse(self.a1.editSelf("NateDog", "iNstRectAr", "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertFalse(self.a1.editSelf("NateDog", self.I, "Natedog@gmail.com", 42, 1010101010))
        self.assertFalse(self.a1.editSelf("NateDog", self.I, "NAT@", "The Trap House", 1010101010))
        self.assertFalse(self.a1.editSelf("NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1))
        # bad parameters for editSelf

        self.a1.editSelf("NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010)
        self.assertEqual(self.a1.user.username, "NateDog")
        self.assertEqual(self.a1.user.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userName, "NateDog")
        self.assertEqual(self.a1.userID, self.I)
        self.assertEqual(self.a1.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userPhone, 1010101010)
        self.assertEqual(self.a1.userAddress, "The Trap House")
        self.a1.editSelf("Nate", self.T, "glasses@gmail.com", "22 Middleton Rd", 1234567890)
        # checks if editSelf worked correctly with correct parameters
        pass

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
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", "iNstRectAr", "Natedog@gmail.com", "The Trap House", 1010101010))
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", self.I, "Natedog@gmail.com", 42, 1010101010))
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", self.I, "NAT@", "The Trap House", 1010101010))
        self.assertFalse(self.a4.editOther(self.a1, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1))
        # returns false for bad parameters given

        self.a4.editOther(self.a1, "NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010)
        self.assertEqual(self.a1.user.username, "NateDog")
        self.assertEqual(self.a1.user.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userName, "NateDog")
        self.assertEqual(self.a1.userID, self.I)
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

class TestCourse(TestCase):

    def setUp(self):
        self.c1 = Course.objects.create("History of Math", 200, "EMS", "MWF", "01:00 - 01:50", "FALL", "ROCK", "LING", 4)
        self.c2 = Course.objects.create("History of Baths", 500, "EBS", "F", "20:00 - 20:50", "FALL", "SOCK", "TING", 15)
        # create our test courses

        self.c2.create(self.c2.name, self.c2.number, self.c2.place, self.c2.days, self.c2.time, self.c2.semester,
                       self.c2.professor, self.c2.ta, self.c2.labs)
        # create user class for c2
        pass

    def testCreate(self):
        self.assertEqual(self.c1.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                       self.c1.professor, self.c1.ta, self.c1.labs), "Course was created")
        # should return this if already exists

        self.c1.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                       self.c1.professor, self.c1.ta, self.c1.labs)
        self.assertEqual(self.c1.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                       self.c1.professor, self.c1.ta, self.c1.labs), "Course already exist")
        # should return this if already exists
        pass

    """
    def testSearch(self):
        self.assertTrue(self.c2.search("History of Baths"))
        # should be true

        self.assertFalse(self.c2.search("History"))
        self.assertFalse(self.c2.search("Chinese Horse Energy"))
        # should both be false
        pass
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
        self.c2.setlabs(1)
        # sets new values

        self.assertEqual(self.c2.name, "Shower Physics")
        self.assertEqual(self.c2.number, 100)
        self.assertEqual(self.c2.place, "Physics Building")
        self.assertEqual(self.c2.days, "MW")
        self.assertEqual(self.c2.time, "12:00 - 12:50")
        self.assertEqual(self.c2.semester, "SPRING")
        self.assertEqual(self.c2.professor, "GLOCK")
        self.assertEqual(self.c2.ta, "PING")
        self.assertEqual(self.c2.labs, 1)
        # checks correctly set

        self.assertFalse(self.c2.setname())
        self.assertFalse(self.c2.setnumber())
        self.assertFalse(self.c2.setplace())
        self.assertFalse(self.c2.setdays())
        self.assertFalse(self.c2.settime())
        self.assertFalse(self.c2.setsemester())
        self.assertFalse(self.c2.setprofessor())
        self.assertFalse(self.c2.setta())
        self.assertFalse(self.c2.setlabs())
        # checks empty set

        self.assertFalse(self.c2.setname(12))
        self.assertFalse(self.c2.setnumber("hi"))
        self.assertFalse(self.c2.setplace(12))
        self.assertFalse(self.c2.setdays(12))
        self.assertFalse(self.c2.settime(12))
        self.assertFalse(self.c2.setsemester(12))
        self.assertFalse(self.c2.setprofessor(12))
        self.assertFalse(self.c2.setta(12))
        self.assertFalse(self.c2.setlabs("hello"))
        # checks incorrectly set

        self.assertTrue(self.c2.search("Shower Physics"))
        self.assertFalse(self.c2.search("History of Baths"))
        # checks updated names in search
        pass

    def testStr(self):
        self.assertEqual(self.c2.tostr(), "History of Baths 500 EBS F 20:00 - 20:50 FALL SOCK TING 15")
        # asserts toStr has correct format
        pass





