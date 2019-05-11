from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account


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
        allUsers = allUsers.order_by("userName")
        currentUser = allUsers.filter(SignInName=username)
        currentUser = currentUser[0]

        # Return all the data gathered above to the HTML page
        return render(request, "main/user.html", {"SignInName": username, "email": email, "password": password,
                                                  "name": name, "phone": phone, "address": address, "groupid": groupid,
                                                  "hours": hours, "allusers": allUsers, "currentUser": currentUser})

    # Post Method:
    # Used to update user information from account page
    def post(self, request):

        request.session.pop("error_messages", None)

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

            if Account.updateUser(user, email, phone, address, hours) is False:
               error_messages = "Some fields did not meet requirements. Try again"
               username = request.session["SignInName"]
               user = Account.get(username)
               allUsers = Account.objects.all()

               return render(request, "main/user.html", {"error_messages": error_messages,
                                                              "SignInName": user.SignInName, "email": user.userEmail,
                                                              "password": user.userPass,
                                                              "name": user.userName, "phone": user.userPhone,
                                                              "address": user.userAddress,
                                                              "groupid": user.groupid, "hours": user.userHours,
                                                              "allusers": allUsers,
                                                              "currentUser": user})

        if 'update_password' in request.POST:
            oldPass = request.POST["oldPass"]
            newPass1 = request.POST["newPass1"]
            newPass2 = request.POST["newPass2"]

            username = request.session["SignInName"]
            user = (Account.objects.all().filter(SignInName=username))[0]

            username = request.session["SignInName"]
            user = Account.get(username)
            allUsers = Account.objects.all()
            return render(request, "main/user.html", {"pass_error_messages": Account.updatePass(user, oldPass, newPass1, newPass2),
                                                          "SignInName": user.SignInName, "email": user.userEmail,
                                                          "password": user.userPass,
                                                          "name": user.userName, "phone": user.userPhone,
                                                          "address": user.userAddress,
                                                          "groupid": user.groupid, "hours": user.userHours,
                                                          "allusers": allUsers,
                                                          "currentUser": user})

        return redirect("user")
