from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Course

# Create your views here.

class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    Lists the courses created by the user(owner).
    fields; 
    """
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Uses a model form to create a new Course object:
    template: form.html; fields; form; owner; success_url
    """
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Allows the editing of an existing Course object.
    fields; template: form.html; form; owner; success_url
    """
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    success_url; fields
    """
    template_name = 'courses/manage/course/delete.html'