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
        newAccount = cls(SignInName=username, userPass=password1, userName=name, userEmail=email, userPhone=phone,
                         userAddress=address, groupid=id, userHours=hours)
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

    @classmethod
    def get(self, name):
        return Account.objects.all().filter(SignInName=name).first()


class Lab(models.Model):
    parentSection = models.CharField(max_length=60)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    ta = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    """
    create lab to be added to a section
    needs parent course name, parent section number, lab number and ta(can be null) 
    """
    @classmethod
    def create(cls, parentCourse, parentSection, labNumber, ta):
        try:
            lab = Lab.search(parentCourse, parentSection, labNumber)
            if lab is False:
                foundTA = Account.get(ta)
                lab = cls(parentSection=parentCourse, number=labNumber, ta=foundTA)
                lab.save()
                section = Section.get(parentCourse, parentSection)
                section.labs.add(lab)
                section.save()
                course = Course.get(parentCourse)
                course.save()
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @classmethod
    def changeta(cls, parentCourse, sectionNum, labNum, newTA):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.ta = newTA
            lab.save()
            return True
        return False

    @classmethod
    def changenumber(cls, parentCourse, sectionNum, labNum, newNum):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.number = newNum
            lab.save()
            return True
        return False

    @classmethod
    def changeplace(cls, parentCourse, sectionNum, labNum, newPlace):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.place = newPlace
            lab.save()
            return True
        return False

    @classmethod
    def changedays(cls, parentCourse, sectionNum, labNum, newDays):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.days = newDays
            lab.save()
            return True
        return False

    @classmethod
    def changetime(cls, parentCourse, sectionNum, labNum, newTime):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.time = newTime
            lab.save()
            return True
        return False

    """
    returns the lab of a section given course name and section number and lab number
    """
    @classmethod
    def get(cls, currentCourse, currentSection, currentLab):
        try:
            section = Section.get(currentCourse, currentSection)
            return section.labs.all().filter(number=currentLab).first()
        except:
            return None

    """
    looks for lab in a section
    takes name of course and section number, and lab number
    returns true if lab exist, else otherwise
    """
    @classmethod
    def search(self, currentCourse, currentSection, newLab):
        check = Lab.get(currentCourse, currentSection, newLab)
        if check is not None:
            return True
        else:
            return False

    def __str__(self):
        return str(self.parentSection) + " Lab: " + str(self.number) + " TA: " + str(self.ta)


class Section(models.Model):
    parentCourse = models.CharField(max_length=60)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    instructor = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    labs = models.ManyToManyField(Lab, blank=True)

    """
    Create a section for a course
    """

    @classmethod
    def create(cls, parentCourse, number, instructor):
        try:
            # check if section exist
            section = Section.search(parentCourse, number)
            if section is False:
                # section does not exist so create course
                # get instructor (can be null)
                foundInstructor = Account.get(instructor)
                # create section object
                section = cls(parentCourse=parentCourse, number=number, instructor=foundInstructor)
                # save section object in database
                section.save()
                # get course
                course = Course.get(parentCourse)
                # add section to course
                course.sections.add(section)
                # save course to database
                course.save()
                return True
            # if section exist, return False
            return False
        except Exception as e:
            # helps with figuring out the error
            print(e)
            return e

    @classmethod
    def changein(cls, parentCourse, sectionNum, newProf):
        section = Section.get(parentCourse, sectionNum)
        if section is not None:
            section.instructor = newProf
            section.save()
            return True
        return False

    @classmethod
    def changeplace(cls, currentCourse, currentSectionNum, newPlace):
        section = Section.get(currentCourse, currentSectionNum)
        if section is not None:
            section.place = newPlace
            section.save()
            return True
        return False

    @classmethod
    def changedays(cls, currentCourse, currentSectionNum, newDays):
        section = Section.get(currentCourse, currentSectionNum)
        if section is not None:
            section.days = newDays
            section.save()
            return True
        return False

    @classmethod
    def changetime(cls, currentCourse, currentSectionNum, newTime):
        section = Section.get(currentCourse, currentSectionNum)
        if section is not None:
            section.time = newTime
            section.save()
            return True
        return False

    """
    creates a lab and adds it to the current section
    takes the course name, section number of course, new lab number and lab TA(can be null)
    """

    @classmethod
    def addlab(cls, currentCourse, currentSection, labNum, labTA):
        return Lab.create(currentCourse, currentSection, labNum, labTA)

    """
    returns the section of a course given course name and section number of the course
    """

    @classmethod
    def get(cls, nameofCourse, numofSection):
        try:
            course = Course.get(nameofCourse)
            return course.sections.all().filter(number=numofSection).first()
        except:
            return None

    """
    looks for section in a course
    takes name of course and section number in course
    returns true if section exist, else otherwise
    """

    @classmethod
    def search(cls, currentCourse, newNum):
        check = Section.get(currentCourse, newNum)
        if check is not None:
            return True
        else:
            return False

    def __str__(self):
        return str(self.parentCourse) + ": " + str(self.number) + " Instructor: " + str(self.instructor)


class Course(models.Model):
    """
    Courses Class: The class used to store course objects / edit / create them
    """

    name = models.CharField(max_length=30)
    number = models.IntegerField(default=0)
    semester = models.CharField(max_length=30)
    sections = models.ManyToManyField(Section, blank=True)

    """
    Create a Course
    """

    @classmethod
    def create(cls, name, number, semester):
        has_course = Course()
        has_course = has_course.search(name)
        if has_course:
            return "That course already exists."
        else:
            course = cls(name=name, number=number, semester=semester)
            course.save()
            return course

    @classmethod
    def changename(cls, currentCourse, newName):
        course = Course.get(currentCourse)
        if course is not None:
            course.name = newName
            course.save()
            return True
        return False

    @classmethod
    def changenumber(cls, currentCourse, newNum):
        course = Course.get(currentCourse)
        if course is not None:
            course.number = newNum
            course.save()
            return True
        return False

    @classmethod
    def changesemester(cls, currentCourse, newSemester):
        course = Course.get(currentCourse)
        if course is not None:
            course.name = newSemester
            course.save()
            return True
        return False

    """
    Give the course name, section number, and the instructor(can be null)
    """

    @classmethod
    def addsection(cls, currentCourse, sectionNum, sectionInstructor):
        return Section.create(currentCourse, sectionNum, sectionInstructor)

    """
        Give the course name, returns true if there is one in the database, returns false otherwise
    """

    @classmethod
    def search(cls, name):
        try:
            check = Course.get(name)
        except Course.DoesNotExist:
            check = None

        if check is not None:
            return True
        else:
            return False

    """
            Give the course name, returns the course, otherwise returns None
    """

    @classmethod
    def get(cls, nameofCourse):
        try:
            course = Course.objects.all().filter(name=nameofCourse).first()
            return course
        except:
            return None

    # call Course.objects.all() to get all courses to string
    def __str__(self):
        return str(self.name) + " " + str(self.number) + " " + str(self.semester)
