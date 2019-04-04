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
                                         userAddress = "22 Middleton rd")
        self.a2 = Account.objects.create(userID=self.i, userName="Andres", userEmail="sweatshirt@gmail.com",
                                         userAddress="34 Giannis rd")
        self.a3 = Account.objects.create(userID=self.a, userName="Sean", userEmail="tshirt@gmail.com",
                                         userAddress="13 Brogdon ave")
        self.a4 = Account.objects.create(userID=self.s, userName="Tyler", userEmail="jersey@gmail.com",
                                         userAddress="11 Lopez ct")

    def test_editAccount(self):



