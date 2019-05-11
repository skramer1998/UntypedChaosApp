from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section, Lab


class LabView(View):

    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        user = Account.get(request.session.get("SignInName"))

        info = request.GET.get("info")
        info = info.split('?')

        coursename = info[0]
        course = Course.get(coursename)

        sectionnumber = info[1]
        section = Section.get(coursename, sectionnumber)

        labnumber = info[2]
        lab = Lab.get(coursename, sectionnumber, labnumber)

        return render(request, "main/labview.html", {"currentCourse": course, "currentUser": user,
                                                     "currentSection": section, "currentLab": lab})

    def post(self, request):

        if 'update_lab' in request.POST:
            number = request.POST["number"]
            place = request.POST["place"]
            days = request.POST["days"]
            time = request.POST["time"]

            coursename = request.POST["currentCourse"]
            sectionnumber = request.POST["currentSection"]
            labnumber = request.POST["currentLab"]

            Lab.changedays(coursename, sectionnumber, labnumber, days)
            number = Lab.changenumber(coursename, sectionnumber, labnumber, number)
            Lab.changeplace(coursename, sectionnumber, labnumber, place)
            Lab.changetime(coursename, sectionnumber, labnumber, time)

            info = "/labview/?info="+coursename+"?"+sectionnumber+"?"+number

            return redirect(info)
