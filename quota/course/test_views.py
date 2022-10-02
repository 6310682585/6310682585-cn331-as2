from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Max
from .models import ID, Course, Request, User

from course import views


class CourseViewTestCase(TestCase):

    def setUp(self):
        # create course and quota
        idcourse = ID.objects.create(code="CN331", coursename="soft engr.")
        course = Course.objects.create(subject=idcourse, semester=1, year=2022, seat=2, coursestatus=1)
        student = User.objects.create_user('hermione', 'hermione@granger.com', 'hermionepassword')
        
        Request.objects.create(username=student, course=course.subject)


    def test_homepage_view_status_code(self):
        """ main page view's status code is ok """

        c = Client()
        response = c.get(reverse('hello:index'))
        self.assertEqual(response.status_code, 200)


    # def test_user_login(self):
    #     """ login view's status code is ok """
    #     c = Client()
    #     response = c.post(reverse('users:login'),
    #            {'username': 'hermione', 'password': 'hermionepassword'})
    #     self.assertEqual(response.status_code, 200)




    def test_course_index_view_status_code(self):
        """ course index view's status code is ok """

        c = Client()
        response = c.get(reverse('course:index'))
        self.assertEqual(response.status_code, 200)

    def test_course_index_view_context(self):
        """ course context is correctly set """

        c = Client()
        course = Course.objects.first()

        response = c.get(reverse('course:index'))
        seat = views.available_seat(course)
        
        self.assertTrue((len(response.context['noncourse']) == 1) and 
            (len(response.context['course']) == 0) and
            seat == 1)

    # def test_add_seat_course(self):
    #     """ can add available course"""

    # def test_cannot_add_nonavailable_seat_course(self):
    #     """ cannot add course"""

    # def test_remove_course(self):
    #     """ can remove course"""