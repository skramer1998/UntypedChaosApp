from django.test import TestCase
from FSA.models import Account
from FSA.models import CoursesModel

class TestAccount(TestCase):
    def setUp(self):
        self.t = "TA"
        self.i = "Instructor"
        self.a = "Admin"
        self.s = "Supervisor"

        self.a1 = Account.objects.create(userID = self.t, userName = "Nate", userEmail = "glasses@gmail.com",
                                         userAddress = "22 Middleton rd", userPhone = 1234567890)
        self.a2 = Account.objects.create(userID=self.i, userName="Andres", userEmail="sweatshirt@gmail.com",
                                         userAddress="34 Giannis rd", userPhone = 2121212121)
        self.a3 = Account.objects.create(userID=self.a, userName="Sean", userEmail="tshirt@gmail.com",
                                         userAddress="13 Brogdon ave", userPhone = 4145554444)
        self.a4 = Account.objects.create(userID=self.s, userName="Tyler", userEmail="jersey@gmail.com",
                                         userAddress="11 Lopez ct", userPhone = 4207106969)

    def test_editAccount(self):
        self.a1.create(self.a1.userID, self.a1.userName, self.a1.userEmail, self.a1.userPhone, self.a1.userAddress)
        self.a2.create(self.a2.userID, self.a2.userName, self.a2.userEmail, self.a2.userPhone, self.a2.userAddress)
        self.a3.create(self.a3.userID, self.a3.userName, self.a3.userEmail, self.a3.userPhone, self.a3.userAddress)
        self.a4.create(self.a4.userID, self.a4.userName, self.a4.userEmail, self.a4.userPhone, self.a4.userAddress)

        self.a1.editSelf("NateDog", self.I, "Natedog@gmail.com", "The Trap House", 1010101010)
        self.assertEqual(self.a1.user.username, "NateDog")
        self.assertEqual(self.a1.user.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userName, "NateDog")
        self.assertEqual(self.a1.userID, self.I)
        self.assertEqual(self.a1.userEmail, "Natedog@gmail.com")
        self.assertEqual(self.a1.userPhone, 1010101010)
        self.assertEqual(self.a1.userAddress, "The Trap House")

