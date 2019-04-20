# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View

"""
from FSA.models import Terminal
from django.template.defaultfilters import linebreaksbr
"""

from .models import Account

# Create your views here.

"""
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
    def get(self, request):
        if request.session.get("SignInName"):
            return redirect("user")
        return render(request, "main/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = Account.objects.all().filter(SignInName=username)

        if user.count() == 0 or user[0].userPass != password:
            return render(request, "main/login.html", {"error_messages": "username/password incorrect"})

        request.session["SignInName"] = username
        return redirect("user")


class LogoutView(View):
    def get(self, request):
        request.session.pop("SignInName", None)
        return redirect("login")


class Register(View):
    def get(self, request):
        return render(request, "main/register.html")

    def post(self, request):
        request.session.pop("error_messages", None)

        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        passwordV = request.POST['passwordV']
        name = request.POST["name"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        groupid = request.POST["groupid"]


        check_user = Account.objects.all().filter(SignInName=username)
        if check_user.count() != 0:
            error_messages = "%s exist, please use another username. Contact Supervisor or Administrator for more help." %(username)
            return render(request, "main/register.html", {"error_messages": error_messages})

        if int(groupid) > 2:
            error_messages = "%s is not a valid ID. Contact Supervisor or Administrator for more help." % (groupid)
            return render(request, "main/register.html", {"error_messages": error_messages})

        if Account.objects.all().filter(groupid=1).count() == 1 and groupid == "1":
            error_messages = "ID %s is already active. Contact Supervisor or Administrator for more help." % (groupid)
            return render(request, "main/register.html", {"error_messages": error_messages})

        if Account.objects.all().filter(groupid=2).count() == 1 and groupid == "2":
            error_messages = "ID %s is already active. Contact Supervisor or Administrator for more help." % (groupid)
            return render(request, "main/register.html", {"error_messages": error_messages})

        Account.create(username, name, email, phone, address, password, passwordV, groupid)
        return redirect("login")


class UserView(View):
    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        username = request.session["SignInName"]
        user = Account.objects.all().filter(SignInName=username)
        user = user[0]
        email = user.userEmail
        password = user.userPass
        name = user.userName
        phone = user.userPhone
        address = user.userAddress
        groupid = user.groupid

        allUsers = Account.objects.all()
        textid = None

        return render(request, "main/user.html", {"SignInName": username, "email": email, "password": password,
                                                  "name": name, "phone": phone, "address": address, "groupid": groupid,
                                                  "allusers": allUsers})
