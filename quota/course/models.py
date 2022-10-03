from pickle import FALSE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class ID(models.Model):
    code = models.CharField(max_length=5)
    coursename = models.CharField(max_length=100)

    def __str__(self):
        return f"{ self.code }({ self.coursename })"

class Course(models.Model):
    # subject (link to class ID)
    subject = models.ForeignKey(ID, on_delete=models.CASCADE, related_name="CourseCode")
    
    # semester
    class SemesterStatus(models.IntegerChoices):
        semester_one = 1
        semester_two = 2
        summer = 3
    semester = models.PositiveIntegerField(choices=SemesterStatus.choices)
    
    # year
    year  = models.CharField(max_length=4, help_text="Use format: YYYY")
    
    # seat
    seat  = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999)])
    
    # status: open/ close
    class CStatus(models.IntegerChoices):
        open = 1
        close = 0
    coursestatus = models.IntegerField(choices=CStatus.choices)

    def __str__(self):
        return f"{ self.subject }: semester{ self.semester } year{ self.year }: seat quota[{ self.seat }]: { self.coursestatus })"

class Request(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, related_name="User")
    course = models.ForeignKey(ID, on_delete=models.SET_NULL, related_name="Coursename", blank=True, null=True)

    def __str__(self):
        return f"{ self.username }: course{ self.course }"
