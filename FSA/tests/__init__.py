import unittest


def suite():   
    return unittest.TestLoader().discover("FSA.tests", pattern="*.py")