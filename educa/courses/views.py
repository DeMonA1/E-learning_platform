from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course
from .forms import ModuleFormSet

# Create your views here.

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """Create a formset with the given Course object and
        optional data
        """
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        """
        Takes HTTP request and its patameters and delegate to 
        get() and post() methods which corresponding
        with HTTP POST and GET methods respectively.
        """
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        """
        Build formset and render it to the template with the 
        current Course object
        """
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
    
    def post(self, request, *args, **kwargs):
        """
        If formset.is_valid it saves data in db and redirect by
        manage_course_list url
        """
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, 
                       PermissionRequiredMixin):
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
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Uses a model form to create a new Course object:
    template: form.html; fields; form; owner; success_url
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Allows the editing of an existing Course object.
    fields; template: form.html; form; owner; success_url
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    success_url; fields
    """
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'