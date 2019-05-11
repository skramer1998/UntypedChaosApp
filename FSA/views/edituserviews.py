from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account


class EditUserView(View):

    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        currentUser = Account.get(request.session.get("SignInName"))
        if currentUser is not None:
            if currentUser.groupid > 2:
                return redirect("user")

        info = request.GET.get("info")
        info = info.split('?')
        user = Account.objects.all().filter(userName=info[0]).first

        return render(request, "main/edituser.html", {"user": user})

    def post(self, request):
        if 'update_account' in request.POST:
            email = request.POST["email"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            hours = request.POST["hours"]
            currentUser = request.POST["currentUser"]
            currentUser = Account.get(currentUser)

            Account.updateUser(currentUser, email, phone, address, hours)

            info = "/edituser/?info=" + currentUser.userName
            return redirect(info)
