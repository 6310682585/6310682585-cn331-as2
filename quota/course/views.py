from os import stat
from django.shortcuts import render
from .models import ID, Course, Request
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    course_exclude = Request.objects
    course = course_exclude.filter(username=request.user.id)
    check_course = Course.objects.exclude(subject__in=[i.course.id for i in course]).exclude(coursestatus=0)
    data = []
    
    for i in check_course:
        seat = Request.objects.filter(course=i.subject.id)
        if len(seat) < i.seat:
            data.append(i)

    return render(request, 'course/index.html', {
        'course': course,
        'noncourse': data
    })

def add(request):
    if request.method == "POST":
        courseId = request.POST["course"]
        course = Course.objects.get(pk=courseId)
        is_registered = Request.objects.filter(username=request.user.id).filter(course=course.subject.id)
        if len(is_registered) > 0:
            return HttpResponse('You had been requested.', status = 400)

        if available_seat(course) <= 0:
            return HttpResponse('Seat is full.', status = 400)
        
        if course.coursestatus == 0:
            return HttpResponse('Course is closed.', status = 400)
            
        Request.objects.create(username_id=request.user.id, course_id=course.subject.id)
    return HttpResponseRedirect(reverse('course:index'), status = 200)

def available_seat(course):
    seat = Request.objects.filter(course=course.subject.id)
    return course.seat - len(seat)

def remove(request, request_id):
    course_id = Request.objects.get(pk=request_id).course.id
    courses = Request.objects.filter(username=request.user.id)
    course = Course.objects.get(pk=course_id)
    check = 0

    for i in courses:
        if course_id == i.course.id:
            check+= 1
    
    if check == 0:
        return HttpResponse('You had not requested.', status = 400)
    
    Request.objects.filter(username=request.user.id).filter(course=course.id).delete()
    
    return HttpResponseRedirect(reverse('course:index'), status = 200)