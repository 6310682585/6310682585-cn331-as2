from urllib import request
from django.contrib import admin

from .models import ID, Course, Request

# Register your models here.

admin.site.register(ID)
admin.site.register(Course)
admin.site.register(Request)