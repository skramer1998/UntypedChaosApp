from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course
from collections import OrderedDict


class MySectionsView(View):

    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        user = Account.get(request.session.get("SignInName"))


        info = request.GET.get("info")
        course = Course.get(info)

        SectionsUserIn = []

        allSections = course.sections.all()
        for section in allSections:
            if section.instructor == user:
                SectionsUserIn.append(section)
            allLabs = section.labs.all()
            for lab in allLabs:
                if lab.ta == user:
                    SectionsUserIn.append(section)

        SectionsUserIn = list(OrderedDict.fromkeys(SectionsUserIn))


        # Return all the data to the HTML page
        return render(request, "main/mysections.html",
                      {"allSections": SectionsUserIn, "currentCourse": info})
