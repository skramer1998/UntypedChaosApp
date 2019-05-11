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

        listTA = Account.objects.all().filter(groupid=4)

        return render(request, "main/labview.html", {"currentCourse": course, "currentUser": user,
                                                     "currentSection": section, "currentLab": lab, "taList": listTA})

    def post(self, request):

        if 'update_lab' in request.POST:
            number = request.POST["number"]
            place = request.POST["place"]
            days = request.POST["days"]
            time = request.POST["time"]
            ta = request.POST.get("ta")

            coursename = request.POST["currentCourse"]
            sectionnumber = request.POST["currentSection"]
            labnumber = request.POST["currentLab"]

            number = Lab.changenumber(coursename, sectionnumber, labnumber, number)
            Lab.changedays(coursename, sectionnumber, number, days)
            Lab.changeplace(coursename, sectionnumber, number, place)
            Lab.changetime(coursename, sectionnumber, number, time)
            Lab.changeta(coursename, sectionnumber, number, ta)

            info = "/labview/?info="+coursename+"?"+sectionnumber+"?"+number
            return redirect(info)
