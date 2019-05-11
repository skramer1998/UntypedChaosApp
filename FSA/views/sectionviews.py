from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section


class SectionView(View):

    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        if request.GET.get("info") is None:
            return redirect("courses")

        # get the information passed in ur
        info = request.GET.get("info")
        # split it using '?'
        info = info.split('?')

        # get course name from info
        coursename = info[0]
        # get course
        course = Course.get(coursename)

        # get section number from info
        sectionnumber = info[1]
        # get section
        section = Section.get(coursename, sectionnumber)

        # get a list of all labs in the section
        labList = section.labs.all().order_by("number")

        # get current user
        username = request.session.get("SignInName")
        user = Account.get(username)

        taList = Account.objects.all().filter(groupid=4).order_by("userName")
        instructorList = Account.objects.all().filter(groupid=3).order_by("userName")

        return render(request, "main/sectionview.html", {"currentCourse": course, "currentUser": user,
                                                         "currentSection": section, "labList": labList,
                                                         "taList": taList, "instructorList": instructorList})

    def post(self, request):
        # pressed on create_lab button
        if 'create_lab' in request.POST:
            # getting values
            currentCourse = request.POST["currentCourse"]
            currentSection = request.POST["currentSection"]
            newTA = request.POST.get("ta")
            labNumber = request.POST["number"]
            # adding a lab to the section
            Section.addlab(currentCourse, currentSection, labNumber, newTA)
            info = "/sectionview/?info=" + currentCourse + "?" + currentSection
            return redirect(info)

        if 'update_section' in request.POST:
            number = request.POST["number"]
            place = request.POST["place"]
            days = request.POST["days"]
            time = request.POST["time"]

            coursename = request.POST["currentCourse"]
            sectionnumber = request.POST["currentSection"]

            number = Section.changenumber(coursename, sectionnumber, number)
            Section.changeplace(coursename, number, place)
            Section.changedays(coursename, number, days)
            Section.changetime(coursename, number, time)

            info = "/sectionview/?info=" + coursename + "?" + number
            return redirect(info)
