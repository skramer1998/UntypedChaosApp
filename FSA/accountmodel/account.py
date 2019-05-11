from django.db import models
from django.contrib.auth.models import User
import getpass


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

        return self.save()

    # Method used to update user password, mostly used for instructors and TAs
    def updatePass(self, oldPass, newPass1, newPass2):
        if self.userPass == oldPass:
            if newPass1 == newPass2:
                self.userPass = newPass1
            else:
                return "New passwords do not match."
        else:
            return "Old password is not correct."
        if len(newPass1) > 30:
            return "New Password is too long. Must be under 30 characters."
        self.save()
        return "Password updated successfully."

    @classmethod
    def get(self, name):
        return Account.objects.all().filter(SignInName=name).first()

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(Account, self).save(*args, **kwargs)
        except:
            return False
