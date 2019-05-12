from django.test import TestCase, Client
from FSA.coursemodel.course import Course, Section
from FSA.accountmodel.account import Account

class TestCourseView(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.get('/register/')
        # Create and log in as the Supervisor
        self.c.post('/register/',
                    {'name': 'Phillip', 'email': 'pm@email.com', 'username': 'moss', 'password': 'password',
                     'passwordV': 'password', 'phone': '1234567890', 'address': '123 Sesame Street', 'hours': 'n/a',
                     'groupid': '1'})
        self.c.post('', {'username': 'moss', 'password': 'password'})
        self.c.post('/registerloggedin/',
                    {'name': 'instructor', 'email': 'instructor@email.com', 'username': 'instructor',
                     'phone': '0987654321', 'address': 'default', 'hours': 'Monday 10-11', 'groupid': '3'})
        self.c.get('/courses/')
        self.c.post('/courses/', {'name': 'memology', 'number': '101', 'semester': 'Spring',
                                  'create_course': 'create_course'})
        self.c.get('/courseview/?coursename=memology')

    def test_createnewsection(self):
        self.c.post('/courseview/?coursename=memology', {'create_section': 'create_section',
                                                         'currentCourse': 'memology', 'instructor': 'instructor',
                                                         'number': '400'})
        self.assertEqual(Section.get('memology', '400').number, 400)

    def test_updateinstructor(self):
        self.c.post('/courseview/?coursename=memology', {'create_section': 'create_section',
                                                         'currentCourse': 'memology', 'instructor': 'instructor',
                                                         'number': '400'})
        self.c.post('/courseview/?coursename=memology', {'update_instructor': 'update_instructor',
                                                         'currentCourse': 'memology', 'instructor': '',
                                                         'number': '400'})
        self.assertEqual(Section.get('memology', '400').instructor, None)

        self.c.post('/courseview/?coursename=memology', {'update_instructor': 'update_instructor',
                                                         'currentCourse': 'memology', 'instructor': 'instructor',
                                                        'number': '400'})
        self.assertEqual(Section.get('memology', '400').instructor, Account.get('instructor'))

    def test_updatecourse(self):
        self.c.post('/courseview/?coursename=memology', {'create_section': 'create_section',
                                                         'currentCourse': 'memology', 'instructor': 'instructor',
                                                         'number': '400'})

        self.assertEqual(Section.get('memology', '400').instructor, Account.get('instructor'))
        self.assertEqual(Section.get('memology', '400').number, 400)
