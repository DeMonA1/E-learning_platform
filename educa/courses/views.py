from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course

# Create your views here.

class ManageCourseListView(ListView):
    model = Course
    template_name = 'course/manage/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)