from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account


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