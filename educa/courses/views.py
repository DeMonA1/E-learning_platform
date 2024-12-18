from django.apps import apps
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.cache import cache
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Course, Module, Content, Subject
from students.forms import CourseEnrollForm
from .forms import ModuleFormSet

# Create your views here.


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
    

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        """Create form for the model"""
        Form = modelform_factory(model,
                                 exclude=['owner', 'order', 
                                          'created', 'updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        # text, video,...
        self.model = self.get_model(model_name)
        # id of object which be updated or None, if create new obj
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})
    
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list',
                            self.module.id)
        return self.render_to_response({"form": form,
                                        "object": self.obj})
    

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list',
                        module.id)
    

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})
    

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, 
                      View):
    """
    Change the order of modules via drag and  drop
    """
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                  course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})
    

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, 
                       View):
    """
    Change the order of contents via drag and  drop
    """
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                   module__course__owner=request.user
                                    ).update(order=order)
        return self.render_json_response({'saved': 'OK'})
    

class CourseListView(TemplateResponseMixin, View):
    """
    Allow to see all the courses available on the site
    """
    model = Course
    template_name = 'courses/course/list.html'
    
    def get(self, request, subject=None):
        # annotate adds additional field to each Course instance
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=
                                                Count('courses'))
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.annotate(total_modules=
                                          Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})
    

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # init hidden course field with the current Course obj
        context['enroll_form'] = CourseEnrollForm(
                                    initial={'course': self.object})
        return context