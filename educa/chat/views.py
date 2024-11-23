from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course

# Create your views here.

@login_required
def course_chat_room(request, course_id):
    """
    Access to course chat-room only for enrolled users
    """
    try:
        # retrieve course with given id joined by the current user
        course = request.user.course_joined.get(id=course_id)
    except Course.DoesNotExist:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()  # 403
    return render(request, 
                  'chat/room.html', 
                  {'course': course})


