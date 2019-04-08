from django.test import TestCase
from FSA.models import Account
from FSA.models import Course

class TestAccount(TestCase):
    def setUp(self):
        self.t = "TA"
        self.i = "Instructor"
        self.a = "Admin"
        self.s = "Supervisor"
        # 4 ID's

        self.a1 = Account.objects.create(userID = self.t, userName = "Nate", userEmail = "glasses@gmail.com",
                                         userAddress = "22 Middleton rd", userPhone = 1234567890)
        self.a2 = Account.objects.create(userID=self.i, userName="Andres", userEmail="sweatshirt@gmail.com",
                                         userAddress="34 Giannis rd", userPhone = 2121212121)
        self.a3 = Account.objects.create(userID=self.a, userName="Sean", userEmail="tshirt@gmail.com",
                                         userAddress="13 Brogdon ave", userPhone = 4145554444)
        self.a4 = Account.objects.create(userID=self.s, userName="Tyler", userEmail="jersey@gmail.com",
                                         userAddress="11 Bledsoe ct", userPhone = 4207106969)
        # creates 4 accounts with each level of ID

        self.a1.create(self.a1.userID, self.a1.userName, self.a1.userEmail, self.a1.userPhone, self.a1.userAddress)
        self.a2.create(self.a2.userID, self.a2.userName, self.a2.userEmail, self.a2.userPhone, self.a2.userAddress)
        self.a3.create(self.a3.userID, self.a3.userName, self.a3.userEmail, self.a3.userPhone, self.a3.userAddress)
        self.a4.create(self.a4.userID, self.a4.userName, self.a4.userEmail, self.a4.userPhone, self.a4.userAddress)
        # creates user classes

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

class TestCourse(TestCase):
    def setUp(self):
        self.c1 = Course.objects.create("History of Math", 200, "EMS", "MWF", "01:00 - 01:50", "FALL", "ROCK", "LING", 4)
        self.c2 = Course.objects.create("History of Baths", 500, "EBS", "F", "20:00 - 20:50", "FALL", "SOCK", "TING", 15)
        # create our test courses

        self.c2.create(self.c2.name, self.c2.number, self.c2.place, self.c2.days, self.c2.time, self.c2.semester,
                       self.c2.professor, self.c2.ta, self.c2.labs)
        # create user class for c2

    def testCreate(self):
        self.assertEqual(self.c1.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                       self.c1.professor, self.c1.ta, self.c1.labs), "Course was created")
        # should return this if already exists

        self.c1.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                       self.c1.professor, self.c1.ta, self.c1.labs)
        self.assertEqual(self.c1.create(self.c1.name, self.c1.number, self.c1.place, self.c1.days, self.c1.time, self.c1.semester,
                       self.c1.professor, self.c1.ta, self.c1.labs), "Course already exist")
        # should return this if already exists

    def testSearch(self):
        self.assertTrue(self.c2.search("History of Baths"))
        # should be true

        self.assertFalse(self.c2.search("History"))
        self.assertFalse(self.c2.search("Chinese Horse Energy"))
        # should both be false

    def testSet(self):
        self.c2.setname("Shower Physics")
        self.c2.setnumber()
        self.c2.setplace()
        self.c2.setdays()
        self.c2.settime()
        self.c2.setsemester()
        self.c2.setprofessor()
        self.c2.setta()
        self.c2.labs()


        self.assertTrue(self.c2.search("Shower Physics"))
        self.assertFalse(self.c2.search("History of Baths"))
        # checks updated names in search

    def testStr(self):
        self.assertEqual(self.c2.tostr(), "History of Baths 500 EBS F 20:00 - 20:50 FALL SOCK TING 15")
        # asserts toStr has correct format

