from django.test import TestCase, Client
from FSA.coursemodel.course import Course

"""
ACCEPTANCE TEST CLASSES AT THE BOTTOM
"""


class TestCourses(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.get('/register/')
        # Create and log in as the Supervisor
        self.c.post('/register/',
                    {'name': 'Phillip', 'email': 'pm@email.com', 'username': 'moss', 'password': 'password',
                     'passwordV': 'password', 'phone': '1234567890', 'address': '123 Sesame Street', 'hours': 'n/a',
                     'groupid': '1'})
        self.c.post('', {'username': 'moss', 'password': 'password'})
        self.c.get('/registerloggedin/')
        # Create an instructor and a TA to use
        self.c.post('/registerloggedin/',
                    {'name': 'instructor', 'email': 'instructor@email.com', 'username': 'instructor',
                     'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11', 'groupid': '3'})
        self.c.get('/registerloggedin/')
        self.c.post('/registerloggedin/',
                    {'name': 'ta', 'email': 'ta@email.com', 'username': 'ta', 'phone': '0987654321',
                     'address': 'default', 'hours': 'Monday 10-11', 'groupid': '4'})
        self.c.get('/courses/')

    def test_failCreate(self):
        # Try making a course using Instructor and TA that don't exist
        response = self.c.post('/courses/', {'name': 'memology', 'number': '101', 'place': 'here', 'days': 'MWF',
                                             'time': 'whenever', 'semester': 'Spring', 'Professor': 'Overlord Rico',
                                             'TA': 'Rico Jr.'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.object.all(), 0)

    def test_Create(self):
        # And again using the existing accounts
        response = self.c.post('/courses/', {'name': 'memology', 'number': '101', 'place': 'here', 'days': 'MWF',
                                             'time': 'whenever', 'semester': 'Spring', 'Professor': 'instructor',
                                             'TA': 'ta'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.object.all(), 1)

    def test_CreateExisting(self):
        # Set up by first creating a course
        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'place': 'here', 'days': 'MWF',
                                  'time': 'whenever', 'semester': 'Spring', 'Professor': 'instructor',
                                  'TA': 'ta'})
        self.assertEqual(Course.object.all(), 1)
        self.c.get('/courses/')
        # Now attempt to create a course that already exists
        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'place': 'here', 'days': 'MWF',
                                  'time': 'whenever', 'semester': 'Spring', 'Professor': 'instructor',
                                  'TA': 'ta'})
        self.assertEqual(Course.object.all(), 1)