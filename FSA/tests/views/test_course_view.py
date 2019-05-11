from django.test import TestCase, Client
from FSA.coursemodel.course import Course


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
        self.c.get('/courses/')

    def test_failCreate(self):
        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'semester': 'Spring',
                                  'create_course': 'create_course'})
        self.c.post('/courses/', {'name': ' ', 'number': 0, 'semester': ' ',
                                  'create_course': 'create_course'})

        self.assertEqual(Course.objects.all().count(), 1)

    def test_Create(self):
        # And again using the existing accounts
        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'semester': 'Spring',
                                  'create_course': 'create_course'})
        self.assertEqual(Course.objects.all().count(), 1)

        self.c.post('/courses/', {'name': 'classology', 'number': '100', 'semester': 'Spring',
                                  'create_course': 'create_course'})
        self.assertEqual(Course.objects.all().count(), 2)

    def test_CreateExisting(self):
        # Set up by first creating a course
        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'semester': 'Spring',
                                  'create_course': 'create_course'})
        self.assertEqual(Course.objects.all().count(), 1)

        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'semester': 'Spring',
                                  'create_course': 'create_course'})
        self.assertEqual(Course.objects.all().count(), 1)
