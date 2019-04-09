# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import getpass

# User object
user = None


# Create your models here.
class Terminal(models.Model):

    """
    Terminal Class: The class used to make the webpage comamnd line work correctly
    """

    """
    Function called by the Home view, immediately passes input to the command parser.
    """
    def command(self, input_string):
        command_string = input_string
        return self.parseCommand(command_string)

    """
    Parse the given input string based on whitespace.
    Check to see if the user is trying to login, if they are follow protocol, if they are not check to see if
    they are already logged in.  IF they are not tell them to login.  IF they are, continue on processing
    the parsed command.
    """
    def parseCommand(self, cmdStr):
        global user
        parseCmd = cmdStr.split()
        print(parseCmd[0].lower())
        print(user)
        if parseCmd[0].lower() == 'login':
            if len(parseCmd) > 2:
                return self.login(parseCmd[1], parseCmd[2])
            else:
                return "You need to provide login arguments!"
        else:
            if user is None:
                return "You are not logged in, you must login before entering commands."
            elif parseCmd[0].lower() == 'createaccount':
                if len(parseCmd) > 9:
                    #  print("branch 1")
                    return self.createaccount(parseCmd[1], "" + parseCmd[2] + " " + parseCmd[3] + " " + parseCmd[4],
                                              parseCmd[5], parseCmd[6], parseCmd[7], parseCmd[8], parseCmd[9])
                elif len(parseCmd) > 8:
                    #  print("branch 2")
                    return self.createaccount(parseCmd[1], "" + parseCmd[2] + " " + parseCmd[3], parseCmd[4],
                                              parseCmd[5], parseCmd[6], parseCmd[7], parseCmd[8])
                else:
                    return "not enough args to create account"
            elif parseCmd[0].lower() == 'accountlist':
                return self.accountList()
            elif parseCmd[0].lower() == 'logout':
                return self.logout()
            elif parseCmd[0].lower() == 'createcourse':
                if len(parseCmd) > 9:
                    return self.createCourse(parseCmd[1], parseCmd[2], parseCmd[3], parseCmd[4],
                                             parseCmd[5], parseCmd[6], parseCmd[7], parseCmd[8], parseCmd[9])
                else:
                    return "not enough args to create a new course"
            else:
                return "You are logged in, cool. Here's the help page, as your command didn't match anything else\n"\
                       + self.help()

    """
    Print out the list of user accounts by SignInName.
    """
    def accountList(self):
        return "Account List: " + ", ".join(list(Account.objects.values_list('userName', flat=True)))

    """
    Create the password for new accounts.
    """
    def setNewPassword(self, npuser, passwordAttempt1, passwordAttempt2 ):  # CAN'T BE CALLED DIRECTLY
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
            print("user has a usable password, \
            can't set new password with this function. use the account(.) something or other")
            return self

    def help(self):
        return "FSA help\nCommands: \nlogin-- sign into an existing account.\nusage: login Username Password\n\
              logout-- sign out from your account\nusage: logout\ncreateAccount-- makes a new account, \
              default permissions none.\nusage: createAccount SignInName FirstName [MiddleName(optional)] \
              LastName Email Phone Address NewAccountpassword NewAccountpassword\naccountList-- \
              returns a list of all accounts\nusage: accountList\ncreateCourse-- creates a new course\n\
              usage: createCourse name #number# place days time semester professor ta #OfLabs\n\
              listCourses-- lists all courses\nusage: listCourses"


    """
    Create a new account.
    """
    def createaccount(self, SignInName, name, email, phone, address, password1, password2):
        Account.create(SignInName, name, email, phone, address, password1, password2)
        return "Your account was successfully created! You were also signed in."

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
            # look up username
            # if username is real, get password
            # validate password
            # if correct, set user equal to the account
            # if incorrect, print "wrong password" and end the function call
            # password = getpass.getpass()

    def logout(self):
        global user
        if user is None:
            #print("you aren't logged in, so you can't log out")
            return "You aren't logged in, so you can't log out."
        else:
            user = None
            #print("logged out")
            #print(self.user)
            return "You have been logged out."

    def createCourse(self, name, number, place, days, time, semester, professor, ta, labs):
        print("called into create Course")
        return Course.create(name, number, place, days, time, semester, professor, ta, labs)


class Course(models.Model):
    # need to change later. Lab class? courses can have more than one lab and more than one ta
    name = models.CharField(max_length=30)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)
    professor = models.CharField(max_length=30)
    ta = models.CharField(max_length=30)
    labs = models.IntegerField(default=0)

    @classmethod
    def create(cls, name, number, place, days, time, semester, professor, ta, labs):
        print("got into course.create")
        if Course.objects.filter(name__contains=name).first() is not None:
            return "Course already exist"
        else:
            print("got into the else")
            newThing = Course.cls(Course(Course), name=name, number=number, place=place, days=days, time=time, semester=semester, professor=professor,
                                  ta=ta, labs=labs)
            print(len(Course.objects.all()))
            return "Course was created"

    def cls(self, name, number, place, days, time, semester, professor, ta, labs):
        print("got into cls")
        almost_course = Course.objects.create(name=name, number=number, place=place, days=days,
                                              time=time, semester=semester, professor=professor,
                                              ta=ta, labs=labs)
        """self.name = name
        self.number = number
        self.place = place
        self.days = days
        self.time = time
        self.semester = semester
        self.professor = professor
        self.ta = ta
        self.labs = labs"""
        print(almost_course)
        almost_course.save()
        return almost_course

    def search(self, name):
        if Course.objects.filter(name__contains=name).first() is not None:
            return True
        else:
            return False

    def setname(self, new_name):
        self.name = new_name

    def setnumber(self, new_number):
        self.number = new_number

    def setplace(self, new_place):
        self.place = new_place

    def setdays(self, new_days):
        self.days = new_days

    def settime(self, new_time):
        self.time = new_time

    def setsemester(self, new_semester):
        self.semester = new_semester

    def setprofessor(self, new_professor):
        self.professor = new_professor

    def setta(self, new_ta):
        self.ta = new_ta

    def setlabs(self, new_labs):
        self.labs = new_labs


    # convert to string one course
    def tostr(self):
        return self.name + " " + self.number + " " + self.place + " " + self.days + " " + self.time + " " + self.semester + " " + self.professor + " " + self.ta + "" + self.labs

    # call Course.objects.all() to get all courses to string
    def __str__(self):
        return self.name + " " + self.number + " " + self.place + " " + self.days + " " + self.time + " " + self.semester + " " + self.professor + " " + self.ta + "" + self.labs


class Account(models.Model):
    SignInName = models.CharField(max_length=30)
    userName = models.CharField(max_length=50)
    userEmail = models.CharField(max_length=30)
    userPhone = models.CharField(max_length=30)
    userAddress = models.CharField(max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Associated Auth User+")

    @classmethod
    def create(cls, userid, username, email, phone, address, password1, password2):
        print("go t into create")
        '''x = username.split()
        if len(x) == 2:
              return cls(SignInName=userid, first=x[0], middle="", last=x[1], email=email, phone=phone, address=address)
        else:
              return cls(SignInName=userid, first=x[0], middle=x[1], last=x[2], email=email, phone=phone, address=address)
        '''
        return Account.cls(Account(cls), userid, username, email, phone, address, password1, password2)

    def cls(self, othernameforid, username, email, userPhone, address, password1, password2):
        if Account.objects.filter(SignInName=othernameforid).first() is not None:
            return "That username is already in use, please select a different one."
            #return self
        print("ayyo let's create some shit")
        print(hash(othernameforid))
        user = User.objects.create_user(username=othernameforid, email=email)  # '''id=len(User.objects.all())+1,'''
        account = Account.objects.create(SignInName=othernameforid,
                                         userName=username, userEmail=email, userPhone=userPhone, userAddress=address,
                                         user_id=user.id)
        #user_id=hash(othernameforid)
        #  user_id cannot be trusted to set itself. creating an accout where the username hashes to the same value as
        #  an existing account will fail.
        terminal = Terminal()
        terminal.setNewPassword(npuser=user, passwordAttempt1=password1, passwordAttempt2=password2)
        account.user = user
        print(account)
        print(account.user)
        print(len(User.objects.all()))
        x = username.split()
        account.user.first_name = x[0]
        account.user.last_name = x[1] if len(x) == 2 else x[2]
        account.user.save()
        account.save()
        return account
        # create an account in the user DB. No password at first, default permissions for user are none, individual
        # group status should be set in a later step.

        # should return false if not set otherwise true

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

    def editSelf(self, name, id, email, phone, address):
        self.user.userid = id
        self.user.username = name
        self.user.userEmail = email
        self.userName = name
        self.userID = id
        self.userEmail = email
        self.userPhone = phone
        self.userAddress = address
        self.user.save()
        # should return false if not set otherwise true

    def is_TA(self, user):
        return user.user.groups.filter(name='ta').exists()

    def is_Instructor(self, user):
        return user.user.groups.filter(name='instructor').exists()

    def is_Admin(self, user):
        return user.user.groups.filter(name='admin').exists()

    def is_Supervisor(self, user):
        return user.user.groups.filter(name='supervisor').exists()

    def grantGroupStatus(self, user, groupName):  # supervisors and admins can grant permissions
        groupName = groupName.lower()
        if Account.is_Supervisor(self):
            if groupName == "ta" or groupName == "instructor" or groupName == "admin" or groupName == "supervisor":
                user.user.group.add(groupName)
                user.user.save()
                print(user.userName + " has been added to "+ groupName +" role")
                return True
            else:
                print("that's not a group. the 4 groups are TA, Instructor, Admin, and Supervisor")
                return False
        elif Account.is_Admin(self):
            if groupName == "ta" or groupName == "instructor" or groupName == "admin":
                user.user.group.add(groupName)
                user.user.save()
                print(user.userName + " has been added to "+ groupName)
                return True
            elif groupName == "supervisor":
                print("Admin accounts cannot add Supervisor status")
                return False
            else:
                print("that's not a group. the 4 groups are TA, Instructor, Admin, and Supervisor")
                return False
        else:
            print("sign in as an Admin or Supervisor to grant group assignments")

    def invalidatePassword(self, user):
        if Account.is_Admin(self) or Account.is_Supervisor(self):
            user.user.setUnusablePassword()
            user.user.save()
            return True
        else:
            print("only Admins and Supervisors can invalidate passwords")
            return False

    def editOther(self, user, name, id, email, phone, address):
        if Account.is_Admin(self) or Account.is_Supervisor(self):
            user.user.username = name
            user.user.userEmail = email
            user.userName = name
            user.userID = id
            user.userEmail = email
            user.userPhone = phone
            user.userAddress = address
            user.user.save()
            print("changes made")
            return True
        else:
            print("only Admins and Supervisors can edit the account details of others")
            return False
        # should return false if not set otherwise true

    def createCourse(self, otherargs):
        if Account.is_Admin(self) or Account.is_Supervisor(self):
            # call course constructor
            return True
        else:
            print("Only Admins and Supervisors can add new Courses")
            return False

    def modifyCourse(self, course, otherargs):
        return False
        # pass shit to course edit method, if self has the permissions to do so.

    def publicInfo(self, user):
        stringofinfo = "Name: " + user.username + "\nEmail: " + user.userEmail + "\nUser ID: " + user.userID
        if Account.is_Admin(self) or Account.is_Supervisor(self):
            stringofinfo += "\nPhone Number:" + user.userPhone + "\nAddress: " + user.userAddress
        return stringofinfo
        # prints the user's public information, and gives the extra private fields if permissions allow
        # wasn't sure if the private info should be its own method or not, so I did it like this

    def toString(self):
        return "User ID: "+self.userID+"\nUsername: "+self.user.username+"\nUserEmail: " + \
               self.user.userEmail+"\nUserPhone: "+self.userPhone+"\nUser Address: "+self.userAddress


