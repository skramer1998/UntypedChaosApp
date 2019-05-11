from django.test import TestCase
from FSA.accountmodel.account import Account


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