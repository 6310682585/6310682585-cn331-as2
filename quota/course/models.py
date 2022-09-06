from django.db import models

# Create your models here.

class ID(models.Model):
    code = models.CharField(max_length=5)
    coursename = models.CharField(max_length=100)

    def __str__(self):
        return f"{ self.code }({ self.coursename })"

class Course(models.Model):
    subject = models.ForeignKey(ID, on_delete=models.CASCADE, related_name="CourseCode")
    semester = models.IntegerField()
    year  = models.IntegerField()
    seat  = models.IntegerField()
    class CStatus(models.IntegerChoices):
        open = 1
        close = 0
    coursestatus = models.IntegerField(choices=CStatus.choices)

    def __str__(self):
        return f"{ self.subject }: semester{ self.semester } year{ self.year }: seat quota[{ self.seat }]: { self.coursestatus })"