from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account


class Register(View):
    """
    Register:
        This is the view that will be processed by new users to the system, but is only used to create Supervisor
        or Administrator accounts.
    """

    # Get Method:
    # Process registration access, redirect as necessary (Gonna need @Andres to update this method comment)
    def get(self, request):

        if 'SignInName' in request.session:
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