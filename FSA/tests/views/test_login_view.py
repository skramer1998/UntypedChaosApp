from django.test import TestCase, Client
from FSA.accountmodel.account import Account


# Acceptance test classes
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