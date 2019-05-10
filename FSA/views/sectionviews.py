from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section


class SectionView(View):

    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

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
        labList = section.labs.all()

        # get current user
        username = request.session.get("SignInName")
        user = Account.get(username)

        return render(request, "main/sectionview.html", {"currentCourse": course, "currentUser": user,
                                                         "currentSection": section, "labList": labList})

    def post(self, request):
        # pressed on create_lab button
        if 'create_lab' in request.POST:
            # getting values
            currentCourse = request.POST["currentCourse"]
            currentSection = request.POST["currentSection"]
            newTA = request.POST["ta"]
            labNumber = request.POST["number"]
            # adding a lab to the section
            Section.addlab(currentCourse, currentSection, labNumber, newTA)

            # Get user
            username = request.session.get("SignInName")
            user = Account.get(username)

            # Get current section
            section = Section.get(currentCourse, currentSection)

            # Get updated lablist
            labList = section.labs.all()

        return render(request, "main/sectionview.html", {"currentCourse": Course.get(currentCourse), "currentUser": user,
                                                         "currentSection": section, "labList": labList})
