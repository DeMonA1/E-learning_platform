from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from courses.models import Course
from .forms import CourseEnrollForm
from .utils import get_redis_connection

# Create your views here.

class StudentRegistrationView(CreateView):
    """
    Registration for new users and after success an 
    user will login automatically.
    """
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result
    

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    
    # equal success_url attr
    def get_success_url(self):
        return reverse_lazy('student_course_detail', 
                            args=[self.course.id])
    

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs =  super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    

class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        redis_conn = get_redis_connection()

        # init the Redis key for the student
        redis_key = f'modules_accessed:{self.request.user.id}'
        
        if 'module_id' in self.kwargs:
            module_id = self.kwargs['module_id']
            context['module'] = get_object_or_404(
                course.modules.all(), id=module_id)
            
            # store accessed module ID in Redis
            redis_conn.sadd(redis_key, module_id)
        else:
            module_first = course.modules.first()
            context['module'] = module_first
            redis_conn.sadd(redis_key, module_first.id)
        
        # fetch all modules accessed by the student
        accessed_modules = redis_conn.smembers(redis_key)
        # bytes to int
        context['accessed_modules'] = [int(m) for m in accessed_modules]
        return context