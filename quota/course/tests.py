from django.test import TestCase
from .models import ID, Course, Request, User
from course import views

class CourseTestCase(TestCase):

    def setUp(self):
        # create course id
        idcourse = ID.objects.create(code="CN201", coursename="OOP")

        Course.objects.create(subject=idcourse, semester=1, year=2022, seat=2, coursestatus=1)

    def test_seat_available(self):
        """ is_seat_available should be True """

        course = Course.objects.first()
        seat = views.available_seat(course)

        self.assertTrue(seat > 0)

    def test_seat_not_available(self):
        """ is_seat_available should be False """
        
        course = Course.objects.first()

        # user1
        User.objects.create_user('harry', 'harry@potter.com', 'harrypassword')
        self.client.login(username = 'harry', password = 'harrypassword')
        
        self.client.post('/course/add/', {
            'course': course,
        })
        self.client.logout()

        # user2
        User.objects.create_user('hermione', 'hermione@granger.com', 'hermionepassword')
        self.client.login(username = 'hermione', password = 'hermionepassword')
        self.client.post('/course/add/', {
            'course': course,
        })
        self.client.logout()

        # check seat
        seat = views.available_seat(course)
        self.assertFalse(seat == 0)