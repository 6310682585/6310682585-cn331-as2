from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('remove/<int:request_id>', views.remove, name='remove'),
]