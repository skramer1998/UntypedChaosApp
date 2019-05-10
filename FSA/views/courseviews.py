from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course


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

        return render(request, "main/courseview.html", {"currentCourse": course, "currentUser": user,
                                                        "listSection": listSection})

    def post(self, request):
        # pressed on create_section
        if 'create_section' in request.POST:
            # get values
            currentCourse = request.POST["currentCourse"]
            newInstructor = request.POST["instructor"]
            sectionNumber = request.POST["number"]

            # add section to course
            Course.addsection(currentCourse, sectionNumber, newInstructor)

            # Get user
            username = request.session.get("SignInName")
            user = Account.objects.all().filter(SignInName=username).first()

            # Get updated sections
            course = Course.get(currentCourse)
            listSection = course.sections.all()

        return render(request, "main/courseview.html", {"currentCourse": Course.get(currentCourse), "currentUser": user,
                                                        "listSection": listSection})