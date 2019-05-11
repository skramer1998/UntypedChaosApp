from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section
from collections import OrderedDict


class MyLabsView(View):

    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        user = Account.get(request.session.get("SignInName"))
        info = request.GET.get("info")
        info = info.split('?')
        course = Course.get(info[0])
        section = Section.get(course.name, info[1])

        LabUserIn = []

        allLabs = section.labs.all()
        for lab in allLabs:
            if lab.ta == user:
                LabUserIn.append(lab)

        LabUserIn = list(OrderedDict.fromkeys(LabUserIn))

        if user.groupid == 3:
            LabUserIn = allLabs

        # Return all the data to the HTML page
        return render(request, "main/mylabs.html",
                      {"allLabs": LabUserIn, "currentCourse": info[0], "currentSection": info[1]})
