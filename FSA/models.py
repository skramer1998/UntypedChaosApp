# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import getpass


"""
class Terminal(models.Model):
    
    Terminal Class: The class used to make the webpage command line work correctly
  

   
    Function called by the Home view, immediately passes input to the command parser.
    

    def command(self, input_string):
        command_string = input_string
        return self.parseCommand(command_string)

    
    Parse the given input string based on whitespace.
    Check to see if the user is trying to login, if they are follow protocol, if they are not check to see if
    they are already logged in.  IF they are not tell them to login.  IF they are, continue on processing
    the parsed command.
    

    def parseCommand(self, cmdStr):
        parseCmd = cmdStr.split()
        print(parseCmd[0].lower())
        print(user)
        if parseCmd[0].lower() == 'login':
            if len(parseCmd) > 2:
                return self.login(parseCmd[1], parseCmd[2])
            else:
                return "You need to provide login arguments!"
        elif parseCmd[0].lower() == 'createaccount':
            if len(parseCmd) > 10:
                #  print("branch 1")
                if 4 < int(parseCmd[10]) < 1:
                    return "Invalid groupID"
                return self.createaccount(parseCmd[1], "" + parseCmd[2] + " " + parseCmd[3] + " " + parseCmd[4],
                                          parseCmd[5], parseCmd[6], parseCmd[7], parseCmd[8], parseCmd[9], parseCmd[10])
            elif len(parseCmd) > 9:
                #  print("branch 2")
                if 4 < int(parseCmd[9]) < 1:
                    return "Invalid groupID"
                return self.createaccount(parseCmd[1], "" + parseCmd[2] + " " + parseCmd[3], parseCmd[4],
                                          parseCmd[5], parseCmd[6], parseCmd[7], parseCmd[8], parseCmd[9])
            else:
                return "not enough args to create account"
        else:
            if user is None:
                return "You are not logged in, you must login before entering commands."
            elif parseCmd[0].lower() == 'accountlist':
                return self.accountList()
            elif parseCmd[0].lower() == 'courselist':
                return self.courseList()
            elif parseCmd[0].lower() == 'logout':
                return self.logout()
            elif parseCmd[0].lower() == 'createcourse':
                if len(parseCmd) > 8:
                    return self.createCourse(parseCmd[1], parseCmd[2], parseCmd[3], parseCmd[4],
                                             parseCmd[5], parseCmd[6], parseCmd[7], parseCmd[8])
                else:
                    return "not enough args to create a new course"
            elif parseCmd[0].lower() == 'assignin':
                if len(parseCmd) > 2:
                    return self.assignmentin(parseCmd[1], parseCmd[2])
            elif parseCmd[0].lower() == 'assignta':
                if len(parseCmd) > 2:
                    return self.assignmentta(parseCmd[1], parseCmd[2])
            else:
                return self.help()

   
    Print out the list of user accounts by userName.
   

    def accountList(self):
        return "Account List: " + ", ".join(list(Account.objects.values_list('userName', flat=True)))

    def courseList(self):
        return Course.objects.all()

    
    Create the password for new accounts. This is an internal function, not to be called directly.
   

    def setNewPassword(self, npuser, passwordAttempt1, passwordAttempt2):
        global user
        if not npuser.has_usable_password():
            while True:
                if passwordAttempt1 == passwordAttempt2:
                    npuser.set_password(passwordAttempt1)
                    npuser.save()
                    user = npuser
                    return "Account password set correctly"
                else:
                    return "Your passwords don't match, please try again."
        else:
            return "user has a usable password, \
            can't set new password with this function. use the account(.) something or other"

   
    A list of all commands, what they do, and how to use them.
   

    def help(self):
        return "Commands: \n----------------\
              \n\nlogin-- sign into an existing account.\nusage: login Username Password\
              \n\nlogout-- sign out from your account\nusage: logout\
              \n\ncreateaccount-- makes a new account, default permissions none.\nusage: createaccount SignInName\
              FirstName [MiddleName(optional)] LastName Email Phone Address NewAccountpassword NewAccountpassword\
              groupID\ngroupID values: 1-supervisor, 2-administrator, 3-instructor, 4-TA\
              \n\naccountlist-- returns a list of all accounts\nusage: accountlist\
              \n\ncreatecourse-- creates a new course\nusage: createcourse name number place days time semester\
              professor ta\
              \n\ncourselist-- lists all courses\nusage: courselist\
              \n\nassignin-- assigns an instructor to a course\nusage: assignin coursename newprofessor\
              \n\nassignta-- assigns a TA to a course\nusage: assignta coursename newta"

   
    Create a new account.
    

    def createaccount(self, SignInName, name, email, phone, address, password1, password2, groupid):

        if groupid == '1':
            if Account.objects.filter(groupid=1).first() is not None:
                return "There is already a supervisor "
        if groupid == '2':
            if Account.objects.filter(groupid=2).first() is not None:
                return "There is already an administrator"
        Account.create(SignInName, name, email, phone, address, password1, password2, groupid)
        return "Your account was successfully created! You were also signed in."

   
    Login to an existing account.
    

    def login(self, username, password):
        global user
        if user is not None:
            return "You're already signed in.  You must logout before you can re-sign in."
        else:
            almostuser = Account.objects.filter(SignInName=username).first()
            if almostuser is None:
                return "No user exists with that username."
            else:
                almostuser = almostuser.user
                if not almostuser.has_usable_password():
                    return self.setNewPassword(almostuser)
                elif almostuser.check_password(password):
                    user = almostuser
                    return username + " successfully logged in."
                else:
                    return "Incorrect password entered."

    
    Logout of currently logged in account, if possible.
    

    def logout(self):
        global user
        if user is None:
            return "You aren't logged in, so you can't log out."
        else:
            user = None
            return "You have been logged out."

    
    Create a course using the given information
    
    def createCourse(self, name, number, place, days, time, semester, professor, ta):
        return Course.create(name, number, place, days, time, semester, professor, ta)

    def assignmentin(self, coursename, newprof):
        Course.assignin(coursename, newprof)
        return "Course instructor has been updated to " + newprof

    def assignmentta(self, coursename, newprof):
        Course.assignta(coursename, newprof)
        return "Course TA has been updated to " + newprof

"""


class Account(models.Model):
    """
    Account Class: The class we're using to store account objects / edit / create them.
    """
    SignInName = models.CharField(max_length=30)
    userPass = models.CharField(max_length=30)
    userName = models.CharField(max_length=50)
    userEmail = models.CharField(max_length=30, blank=True)
    userPhone = models.CharField(max_length=30, blank=True)
    userAddress = models.CharField(max_length=120, blank=True)
    groupid = models.IntegerField(default=0)
    userHours = models.CharField(max_length=100, blank=True)
    """1=SU, 2=AD, 3=IN, 4=TA"""

    """
    Overwrite the generic Account str() function for printing
    """

    def __str__(self):
        return str(self.SignInName)

    @classmethod
    def create(cls, username, name, email, phone, address, password1, password2, id, hours):
        if password1 != password2:
            return "passwords don't match, couldn't create account"
        elif not password1 or not password2:
            return "password cannot be blank"
        newAccount = cls(SignInName=username, userPass=password1, userName=name, userEmail=email, userPhone=phone, userAddress=address, groupid=id, userHours=hours)
        newAccount.save()
        return newAccount

    def editPassword(self):
        # Validate permissions before being able to call this function
        print("type new password: ")
        newPassword = getpass.getpass()
        print("confirm new password: ")
        if newPassword == getpass.getpass():
            if not self.user.has_usable_password():
                self.user.set_password(newPassword)
                self.user.save()
                print("new password set")
            else:
                print("type current password for " + self.user.userid)
                if self.user.check_password(getpass.getpass()):
                    self.user.set_password(newPassword)
                    self.user.save()
                    print("new password set")
                else:
                    print("wrong password for " + self.user.username)
        else:
            print("the new passwords don't match, start again from the beginning.")

    def editSelf(self, userid, username, email, phone, address, password1, password2, id):

        """self.user.userid = id
        self.user.username = name
        self.user.userEmail = email
        self.userName = name
        self.userID = id
        self.userEmail = email
        self.userPhone = phone
        self.userAddress = address
        self.user.save()"""
        return "did not set for this reason: "
        # not updated for working with latest version of account-- will be split up and made to work in next sprint

    def getid(self, account):
        return account.groupid

    # Method used to update user information, currently limited to basic information
    def updateUser(self, email, phone, address, hours):
        if email is not "":
            self.userEmail = email

        if phone is not "":
            self.userPhone = phone

        if address is not "":
            self.userAddress = address

        if hours is not "":
            self.userHours = hours

        self.save()
        return "Account information updated."

    # Method used to update user password, mostly used for instructors and TAs
    def updatePass(self, oldPass, newPass1, newPass2):
        if self.userPass == oldPass:
            if newPass1 == newPass2:
                self.userPass = newPass1
            else:
                return "New passwords do not match."
        else:
            return "Old password is not correct."

        self.save()
        return "Password updated successfully."


# currently labs will not work
class Lab(models.Model):
    number = models.IntegerField(default=0)
    ta = models.ForeignKey(Account, on_delete=models.CASCADE)


class Course(models.Model):
    """
    Courses Class: The class used to store course objects / edit / create them
    """

    # need to change later. Lab class? courses can have more than one lab and more than one ta
    name = models.CharField(max_length=30)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)
    professor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    ta = models.ManyToManyField(Account)

    # labs = models.ForeignKey(Lab, on_delete=models.CASCADE)

    @classmethod
    def create(cls, name, number, place, days, time, semester, professor, ta):
        has_course = Course()
        has_course = has_course.search(name)
        if has_course:
            return "That course already exists."
        else:
            try:
                accountp = Account.objects.filter(SignInName=professor)
                accountp = accountp.first()
                if accountp is None: return "Professor needs to be an account to be assigned to a course."
                temp = Account()
                temp = temp.getid(accountp)
                if temp < 3:
                    return "Administrators and Supervisors cannot be assigned to a course."
            except Account.DoesNotExist:
                accountp = None
            try:
                accountta = Account.objects.filter(SignInName=ta)
                accountta = accountta.first()
                if accountta is None: return "TA needs to be an account to be assigned to a course."
                temp = Account()
                temp = temp.getid(accountta)
                if temp < 4:
                    return "Only TAs can be TAs."
            except Account.DoesNotExist:
                accountta = None

            if accountp is not None:
                if accountta is not None:
                    course = cls(name=name, number=number, place=place, days=days, time=time, semester=semester,
                                 professor=accountp)
                    course.save()
                    course.ta.add(accountta)
                    course.save()
                    return course
            return "Course can not be created."

    def search(self, name):
        try:
            check = Course.objects.get(name=name)
        except Course.DoesNotExist:
            check = None

        if check is not None:
            return True
        else:
            return False

    @classmethod
    def assignin(cls, coursename, newprofessor):
        has_course = Course()
        has_course = has_course.search(coursename)
        if has_course:
            try:
                accountp = Account.objects.filter(SignInName=newprofessor)
                accountp = accountp.first()

            except Account.DoesNotExist:
                accountp = None
            if accountp is not None:
                temp = Account()
                temp = temp.getid(accountp)
                if temp < 3:
                    return "Administrators and Supervisors cannot be assigned to a course."
                currentcourse = Course.objects.filter(name=coursename)
                currentcourse = currentcourse.first()
                currentcourse.professor = accountp
                currentcourse.save()
                return currentcourse
            return "There is no account named " + str(newprofessor)
        return "There is no course named " + str(coursename)

    @classmethod
    def assignta(cls, coursename, newta):
        has_course = Course()
        has_course = has_course.search(coursename)

        print("Assign course called")
        if has_course:
            try:
                accountp = Account.objects.filter(SignInName=newta)
                accountp = accountp.first()
            except Account.DoesNotExist:
                accountp = None
            if accountp is not None:
                temp = Account()
                temp = temp.getid(accountp)
                if temp < 4:
                    return "Administrators and Supervisors cannot be assigned to a course."
                currentcourse = Course.objects.filter(name=coursename)
                currentcourse = currentcourse.first()
                currentcourse.ta.add(accountp)
                """currentcourse.ta = accountp """
                currentcourse.save()

                print(currentcourse.ta.all())

                return currentcourse
            return "There is no account named " + str(newta)
        return "There is no course named " + str(coursename)

    # call Course.objects.all() to get all courses to string
    def __str__(self):
        return str(self.name) + " " + str(self.number) + " " + str(self.place) + " " + str(self.days) + " " + str(
            self.time) + " " + str(self.semester) + " " + str(self.professor) + " " + str(self.ta)
