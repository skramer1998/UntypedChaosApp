# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View

""" DEPRECIATED COMMAND LINE IMPORT
from FSA.models import Terminal
from django.template.defaultfilters import linebreaksbr
"""

from .models import Account

# Create your views here.

""" DEPRECIATED COMMAND LINE VIEW
class Home(View):

    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        yourInstance = Terminal()
        commandInput = request.POST["command"]
        if commandInput:
            response = yourInstance.command(commandInput)
            response = linebreaksbr(response)
        else:
            response = ""
        return render(request, 'main/index.html', {"message": response})

"""


class Login(View):
    """
    Login:
        This is the view that will be processed by all users when they attempt to login.
    """

    # Get Method:
    # Used to check current session, renders user page
    def get(self, request):
        if request.session.get("SignInName"):
            return redirect("user")
        return render(request, "main/login.html")

    # Post Method:
    # Used to log the user in based on information passed from HTML
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = Account.objects.all().filter(SignInName=username)

        # If user does not exist, or the given password is incorrect, return an error message
        if user.count() == 0 or user[0].userPass != password:
            return render(request, "main/login.html", {"error_messages": "username/password incorrect"})

        # If the user exists and the password is correct, set the session to that user
        request.session["SignInName"] = username
        return redirect("user")


class LogoutView(View):
    """
    Logout:
        This is the view that will be processed by all users when they attempt to logout.
    """

    # Get Method:
    # Used to remove the existing user from the session, renders login page
    def get(self, request):
        request.session.pop("SignInName", None)
        return redirect("login")


class RegisterLoggedIn(View):
    """
    RegisterLoggedIn:
        This is the view that will be processed by supervisors when they attempt to make new accounts.
    """

    # Get Method:
    # Renders the registerloggedin page
    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        # next line log outs a user after 5 minutes
        # request.session.set_expiry(300)

        user = request.session.get("SignInName")
        user = (Account.objects.all().filter(SignInName=user))[0]
        user = user.groupid
        if user > 2:
            return render(request, "main/user.html")

        return render(request, "main/registerloggedin.html")

    # Post Method:
    # Takes all account creation info from HTML and checks for validity / creates account
    def post(self, request):
        # Check if the session is in error
        request.session.pop("error_messages", None)

        # Grab HTML form information
        email = request.POST["email"]
        username = request.POST["username"]
        password = username
        passwordV = username
        name = request.POST["name"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        groupid = request.POST['groupid']
        hours = request.POST['hours']

        # Check if the user already exists in the system
        check_user = Account.objects.all().filter(SignInName=username)
        if check_user.count() != 0:
            error_messages = "%s exist, please use another username." % (username)
            return render(request, "main/registerloggedin.html", {"error_messages": error_messages})

        # Check if an Administrator already exists in the system, there can only be 1
        if Account.objects.all().filter(groupid=2).count() == 1 and groupid == "2":
            error_messages = "ID %s is already active. Contact Supervisor or Administrator for more help." % (groupid)
            return render(request, "main/register.html", {"error_messages": error_messages})

        # Create a new account using the previously gained HTML info
        Account.create(username, name, email, phone, address, password, passwordV, groupid, hours)

        # Redirect to the user page
        return redirect("user")


class Register(View):
    """
    Register:
        This is the view that will be processed by new users to the system, but is only used to create Supervisor
        or Administrator accounts.
    """

    # Get Method:
    # Process registration access, redirect as necessary (Gonna need @Andres to update this method comment)
    def get(self, request):

        if request.session.get("SignInName"):
            return render(request, "main/user.html")

        user = request.session.get("SignInName")
        user = (Account.objects.all().filter(SignInName=user))[0]
        user = user.groupid

        check = False
        if Account.objects.all().filter(groupid="1").count() == 1:
            check = True
        if Account.objects.all().filter(groupid="2").count() == 1:
            check = True
        if user == 3:
            check = False
        if user == 4:
            check = False
        if check:
            return redirect("registerloggedin")

        return render(request, "main/register.html")

    # Post Method:
    # Process registration requests from HTML for new Supervisors and Administrators
    def post(self, request):

        # Check for error status
        request.session.pop("error_messages", None)

        # Get HTML information
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        passwordV = request.POST['passwordV']
        name = request.POST["name"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        groupid = request.POST["groupid"]
        hours = request.POST["hours"]

        # Check if the user already exists in the database
        check_user = Account.objects.all().filter(SignInName=username)
        if check_user.count() != 0:
            error_messages = "%s exist, please use another username. Contact Supervisor or Administrator for more help." % (
                username)
            return render(request, "main/register.html", {"error_messages": error_messages})

        # Check if a supervisor already exists while trying to make one
        if Account.objects.all().filter(groupid=1).count() == 1 and groupid == "1":
            error_messages = "ID %s is already active. Contact Supervisor or Administrator for more help." % (groupid)
            return render(request, "main/register.html", {"error_messages": error_messages})

        # Check if an administrator already exists while trying to make one
        if Account.objects.all().filter(groupid=2).count() == 1 and groupid == "2":
            error_messages = "ID %s is already active. Contact Supervisor or Administrator for more help." % (groupid)
            return render(request, "main/register.html", {"error_messages": error_messages})

        # Create a new user once the above checks have passed
        Account.create(username, name, email, phone, address, password, passwordV, groupid, hours)

        # Redirect to login page
        return redirect("login")


class UserView(View):
    """
    UserView:
        This class is used to display the User page
    """

    # Get Method:
    # Used to display user information and more, still IN PROGRESS
    def get(self, request):

        # Check if a user is logged in, if they are not then redirect to login
        if not request.session.get("SignInName"):
            return redirect("login")

        # next line log outs a user after 5 minutes
        # request.session.set_expiry(300)

        # Get all the user info to display to the HTML page
        username = request.session["SignInName"]
        user = (Account.objects.all().filter(SignInName=username))[0]
        email = user.userEmail
        password = user.userPass
        name = user.userName
        phone = user.userPhone
        address = user.userAddress
        groupid = user.groupid
        hours = user.userHours

        # Get all users in DB to display to the HTML page
        allUsers = Account.objects.all()
        currentUser = allUsers.filter(SignInName=username)
        currentUser = currentUser[0]

        # Return all the data gathered above to the HTML page
        return render(request, "main/user.html", {"SignInName": username, "email": email, "password": password,
                                                  "name": name, "phone": phone, "address": address, "groupid": groupid,
                                                  "hours": hours, "allusers": allUsers, "currentUser": currentUser})

    # Post Method:
    # Used to update user information from account page
    def post(self, request):

        # This is a dual-post function
        # It checks to see if it is updating the account or updating the password from the request, and then
        # calls the necessary functions / generates variables from there
        if 'update_account' in request.POST:
            email = request.POST["email"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            hours = request.POST["hours"]

            username = request.session["SignInName"]
            user = (Account.objects.all().filter(SignInName=username))[0]

            Account.updateUser(user, email, phone, address, hours)

        if 'update_password' in request.POST:
            oldPass = request.POST["oldPass"]
            newPass1 = request.POST["newPass1"]
            newPass2 = request.POST["newPass2"]

            username = request.session["SignInName"]
            user = (Account.objects.all().filter(SignInName=username))[0]

            Account.updatePass(user, oldPass, newPass1, newPass2)

        return redirect("user")