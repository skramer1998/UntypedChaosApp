from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course, Section
from django.shortcuts import get_object_or_404


class Courses(View):
    """
    Courses:
        This class is used to display the Course Catalog page
    """

    # Get Method:
    # Used to display course information and more, still IN PROGRESS
    def get(self, request):

        # Check if a user is logged in, if they are not then redirect to login
        if not request.session.get("SignInName"):
            return redirect("login")

        # Get the classes information to display the HTML page
        username = request.session["SignInName"]
        user = (Account.objects.all().filter(SignInName=username)).first()

        """
        DO ACTUAL COURSE STUFF HERE
        """

        # Get all classes in DB to display to the HTML page
        allClasses = Course.objects.all()
        allClasses = allClasses.order_by("number")

        # Return all the data to the HTML page
        return render(request, "main/courses.html",
                      {"SignInName": username, "allClasses": allClasses, "currentUser": user})

    # Post Method:
    # Work in Progress
    def post(self, request):

        # This is a dual-post function
        # It checks to see if it is updating the account or updating the password from the request, and then
        # calls the necessary functions / generates variables from there
        if 'create_course' in request.POST:
            name = request.POST["name"]
            number = request.POST["number"]
            semester = request.POST["semester"]
            Course.create(name, number, semester)
        return redirect("courses")


class CourseView(View):
    def get(self, request):
        if not request.session.get("SignInName"):
            return redirect("login")

        coursename = request.GET.get("coursename")
        course = Course.get(coursename)

        username = request.session.get("SignInName")
        user = Account.objects.all().filter(SignInName=username).first()

        listSection = course.sections.all()
        listSection = listSection.order_by("number")
        instructorList = Account.objects.all().filter(groupid=3)

        return render(request, "main/courseview.html", {"currentCourse": course, "currentUser": user,
                                                        "listSection": listSection, "instructorList": instructorList})

    def post(self, request):
        # pressed on create_section
        if 'create_section' in request.POST:
            # get values
            currentCourse = request.POST["currentCourse"]
            newInstructor = request.POST["instructor"]
            sectionNumber = request.POST["number"]

            # add section to course
            Course.addsection(currentCourse, sectionNumber, newInstructor)

            info = "/courseview/?coursename=" + currentCourse
            return redirect(info)

        # pressed on Update instructor
        if 'update_instructor' in request.POST:
            # get values
            currentCourse = request.POST["currentCourse"]
            newInstructor = request.POST["instructor"]
            sectionNumber = request.POST["number"]

            #Get Instructor
            newIns = Account.objects.all().filter(SignInName=newInstructor).first()

            # Update instructor
            Section.changein(currentCourse, sectionNumber, newIns)

            info = "/courseview/?coursename=" + currentCourse

            if request.POST.get("sectionView") is not None:
                info = "/sectionview/?info=" + currentCourse + "?" + sectionNumber

            return redirect(info)

        if 'update_course' in request.POST:
            currentCourse = request.POST["currentCourse"]
            name = request.POST["name"]
            number = request.POST["number"]
            semester = request.POST["semester"]

            name = Course.changename(currentCourse, name)
            Course.changenumber(name, number)
            Course.changesemester(name, semester)

            info = "/courseview/?coursename=" + name
            return redirect(info)