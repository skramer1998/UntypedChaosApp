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
        return 'Account information updated.'

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
