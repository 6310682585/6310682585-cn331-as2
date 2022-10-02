from django.test import TestCase
from .models import ID, Course, Request, User
from course import views

class CourseTestCase(TestCase):

    def setUp(self):
        # create course id
        idcourse = ID.objects.create(code="CN331", coursename="soft engr.")

        Course.objects.create(subject=idcourse, semester=1, year=2022, seat=2, coursestatus=1)

    def test_seat_available(self):
        """ is_seat_available should be True """

        course = Course.objects.first()
        seat = views.available_seat(course)

        self.assertTrue(seat > 0)

    def test_seat_not_available(self):
        """ is_seat_available should be False """
        
        course = Course.objects.first()

        student1 = User.objects.create_user('harry', 'harry@potter.com', 'harrypassword')
        student2 = User.objects.create_user('hermione', 'hermione@granger.com', 'hermionepassword')
        Request.objects.create(username=student1, course=course.subject)
        Request.objects.create(username=student2, course=course.subject)

        seat = views.available_seat(course)
        self.assertEqual(seat, 0)