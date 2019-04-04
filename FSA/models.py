# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyModel(models.Model):
    fieldOne = models.CharField(max_length=20)
    fieldTwo = models.IntegerField(default=0)
    color = models.CharField(max_length=7)


class AccountModel(models.Model):
    role = models.CharField(max_length=12)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=30)
    userName = models.CharField(max_length=30)
    password = models.CharField(max_length=30)


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


class UserModel(models.Model):
    is_TA = models.BooleanField('TA status', default=False)
    is_Instructor = models.BooleanField('Instructor status', default=False)
    is_Supervisor = models.BooleanField('Supervisor status', default=False)
    is_Admin = models.BooleanField('Admin status', default=False)
# this is how permissions will be handled. This will let us use the same account with multiple permission levels
# it's also less work than user groups, but I can edit this to include them if needed