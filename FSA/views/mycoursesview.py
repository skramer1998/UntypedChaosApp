from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from FSA.accountmodel.account import Account
from FSA.coursemodel.course import Course


class MyCourses(View):
    """
    MyCourses:
        This class is used to display the Course Catalog page for instructors and TAs
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

        CoursesUserIn = []

        # Get all classes in DB with user as the instructor
        allCourses = Course.objects.all()
        for course in allCourses:
            allSections = course.sections.all()
            for section in allSections:
                if section.instructor == user:
                    CoursesUserIn.append(course)
                allLabs = section.labs.all()
                for lab in allLabs:
                    if lab.ta == user:
                        CoursesUserIn.append(course)


        # Return all the data to the HTML page
        return render(request, "main/courses.html",
                      {"SignInName": username, "allClasses": CoursesUserIn, "currentUser": user})

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