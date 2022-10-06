from doctest import REPORT_CDIFF
from urllib import request, response
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
        student = User.objects.create_user(username='hermione', email='hermione@granger.com', password='hermionepassword')
        
        Request.objects.create(username=student, course=course.subject)
        
# test login logout

    def test_homepage_view_status_code(self):
        """ main page view's status code is ok """

        c = Client()
        response = c.get(reverse('hello:index'))
        self.assertEqual(response.status_code, 200)


    def test_user_login(self):
        """ correct username and password can login """
        c = Client()
        response = c.post(reverse('users:login'),
               {'username': 'hermione', 'password': 'hermionepassword'})
        self.assertEqual(response.status_code, 302)

        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_login(self):
        """ wrong username and password cannot login """
        c = Client()
        response = c.post(reverse('users:login'),
               {'username': 'ron', 'password': 'ronpassword'})
        self.assertTrue(response.context['message'] == 'Invalid credentials.')

        response = c.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        """ can logout """
        c = Client()
        response = c.post(reverse('users:logout'))
        self.assertTrue(response.context['message'] == 'you are logged out.')


# test course quota

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

    def test_add_seat_course(self):
        """ can add available course"""

        course = Course.objects.first()
        student = User.objects.create_user(username='draco', email='draco@malfoy.com', password='dracopassword')

        self.client.login(username='draco', password='dracopassword')
        response = self.client.post(reverse('course:add'), {'course': course.subject.id})
        self.assertEqual(response.status_code, 200)


    def test_cannot_add_nonavailable_seat_course(self):
        """ cannot add course"""

        course = Course.objects.first()
        student = User.objects.create_user(username='draco', email='draco@malfoy.com', password='dracopassword')
        student2 = User.objects.create_user( username='harry', email='harry@potter.com', password='harrypassword')
        Request.objects.create(username=student2, course=course.subject)

        self.client.login(username='draco', password='dracopassword')
        response = self.client.post(reverse('course:add'), {'course': course.subject.id})
        self.assertEqual(response.status_code, 400)

    def test_remove_course(self):
        """ can remove course"""

        course = Course.objects.first()
        student = User.objects.create_user(username='draco', email='draco@malfoy.com', password='dracopassword')
        Request.objects.create(username=student, course=course.subject)
        
        self.client.login(username='draco', password='dracopassword')
        response = self.client.post(reverse('course:remove', args=[course.subject.id]))
        self.assertEqual(response.status_code, 200)