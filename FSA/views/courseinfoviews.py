from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section, Lab
from collections import OrderedDict


class CourseInfoView(View):
    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        info = request.GET.get("info")
        info = info.split('?')
        course = Course.get(info[0])
        section = Section.get(course.name, info[1])
        lab = Lab.get(course.name, section.number, info[2])

        user = Account.get(request.session.get("SignInName"))

        taList = []
        allLabs = section.labs.all()
        for lab in allLabs:
            taList.append(lab.ta)

        taList = list(OrderedDict.fromkeys(taList))
        taList.remove(None)

        return render(request, "main/courseinfo.html", {"course": course, "section": section, "lab": lab, "user": user,
                                                        "taList": taList})

    def post(self, request):

        if 'update_ta' in request.POST:
            course = request.POST["currentCourse"]
            section = request.POST["currentSection"]
            lab = request.POST["currentLab"]
            print(lab)
            newTA = request.POST.get("ta")

            Lab.changeta(course, section, lab, newTA)

            info = "/courseinfo/?info=" + course + "?" + section + "?" + lab
            return redirect(info)