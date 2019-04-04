from django.test import TestCase
from FSA.models import AccountModel
from FSA.models import CoursesModel
from FSA.models import UserModel

class TestAccount(TestCase):
    def setUp(self):
        self.a1 = AccountModel.objects.create()
        self.c1 = CoursesModel.objects.create()

    def test_editAccountModel(self):

