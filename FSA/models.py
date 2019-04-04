# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
import getpass


# Create your models here.
class Terminal(models.Model):
    user = None

    def command(self, inStr):
        return self.parseCommand(inStr)

    def parseCommand(self, cmdStr):
        parseCmd = cmdStr.split()
        print(parseCmd[0].lower())
        if parseCmd[0].lower() == 'login':
            return self.login(parseCmd[1])
        else:
            if self.user is None:
                return "You are not logged in, you must login before entering commands."
            else:
                return "You are logged in, cool."

    def setNewPassword(self, user): # CAN'T BE CALLED DIRECTLY
        if not user.has_usable_password():
            while True:
                print("your account currently has no password. You'll have to set it by typing it in twice")
                passwordAttempt1 = getpass.getpass()
                passwordAttempt2 = getpass.getpass()
                if passwordAttempt1 == passwordAttempt2:
                    print("good, you typed the same thing twice. your password is set and good to go")
                    user.set_password(passwordAttempt1)
                    user.save()
                    return
                else:
                    print("those didn't match. Try again")
        else:
            print("user has a usable password, \
            can't set new password with this function. use the account(.) something or other")
            return

    def login(self, username):
        if self.user is not None:
            print("you're already signed in. you have to logout before you can re-sign in.")
        else:
            almostuser = Account.user.filter(userid = 'username')
            if almostuser is None:
                print("no user with that username.")
                return
            else:
                almostuser = almostuser[1]
                if not almostuser.has_usable_password():
                    print("you'll have to set a password before you can login")
                    setNewPassword(almostuser)
                    return
                elif almostuser.check_password(getpass.getpass()):
                    print(username+" is logged in")
                    self.user = almostuser
                    return
                else:
                    print("passwords don't match")
                    return
            # look up username
            # if username is real, get password
            # validate password
            # if correct, set user equal to the account
            # if incorrect, print "wrong password" and end the function call
            #password = getpass.getpass()

    def logout(self):
        if self.user is None:
            print("you aren't logged in, so you can't log out")
            return
        else:
            user = None
            print("logged out")
            return


class MyModel(models.Model):
    fieldOne = models.CharField(max_length=20)
    fieldTwo = models.IntegerField(default=0)
    color = models.CharField(max_length=7)

"""
class AccountModel(models.Model):
    role = models.CharField(max_length=12)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=30)
    userName = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
"""


class CoursesModel(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)
    professor = models.CharField(max_length=30)
    ta = models.CharField(max_length=30)
    labs = models.IntegerField(default=0)


class Account(models.Model):
    userID = models.CharField(max_length=30)
    userName = models.CharField(max_length=50)
    userEmail = models.CharField(max_length=30)
    userAddress = models.CharField(max_length=120)
    #user = models.user # does this work? should be for the actual user part

    @classmethod
    def create(cls, userid, username, email, phone, address):
        x = username.split()
        if x.length() == 2:
            return cls(userid=userid, first=x[0], middle="", last=x[1], email=email, phone=phone, address=address)
        else:
            return cls(userid=userid, first=x[0], middle=x[1], last=x[2], email=email, phone=phone, address=address)

    def cls(self, userid, first, middle, last, email, phone, address):
        self.userID = userid
        self.userName = first + " " + middle + " " + last
        self.userEmail = email
        self.userPhone = phone
        self.userAddress = address
        self.user = models.user.objects.create_user(self.userID, self.userEmail)
        self.user.first_name = first
        self.user.last_name = last
        self.user.groups = None
        self.user.save()
        # create an account in the user DB. No password at first, default permissions for user are none, individual
        # group status should be set in a later step.

        # should return false if not set otherwise true

    def editPassword(self, newPassword):
        # Validate permissions before being able to call this function
        print("confirm new password: ")
        if newPassword == input():
            if not self.user.has_usable_password():
                self.user.set_password(newPassword)
                self.user.save()
                print("new password set")
            else:
                print("type current password for " + self.user.username)
                if self.user.check_password(input()):
                    self.user.set_password(newPassword)
                    self.user.save()
                    print("new password set")
                else:
                    print("wrong password for " + self.user.username)
        else:
            print("the new passwords don't match, start again from the begining.")

    def editSelf(self, name, id, email, phone, address):
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
        return user.user.groups.filter(name='TA').exists()

    def is_Instructor(self, user):
        return user.user.groups.filter(name='Instructor').exists()

    def is_Admin(self, user):
        return user.user.groups.filter(name='Admin').exists()

    def is_Supervisor(self, user):
        return user.user.groups.filter(name='Supervisor').exists()

    def grantGroupStatus(self, user, groupName):  # supervisors and admins can grant permissions
        if Account.is_Supervisor(self):
            if groupName == "TA" or groupName == "Instructor" or groupName == "Admin" or groupName == "Supervisor":
                user.user.group.add(groupName)
                user.user.save()
                print(user.userName + " has been added to "+ groupName)
                return True
            else:
                print("that's not a group. the 4 groups are TA, Instructor, Admin, and Supervisor")
                return False
        elif Account.is_Admin(self):
            if groupName == "TA" or groupName == "Instructor" or groupName == "Admin":
                user.user.group.add(groupName)
                user.user.save()
                print(user.userName + " has been added to "+ groupName)
                return True
            elif groupName == "Supervisor":
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

    def modifyCouse(self, course, otherargs):
        return False
        # pass shit to course edit method, if self has the permissions to do so.

    def publicInfo(self, user):
        return 0
        # big old string with whatever is actually public
        # can include a permissions check ala other methods in this class

    def toString(self):
        return "User ID: "+self.userID+"\nUsername: "+self.user.username+"\nUserEmail: " + \
               self.user.userEmail+"\nUserPhone: "+self.userPhone+"\nUser Address: "+self.userAddress


