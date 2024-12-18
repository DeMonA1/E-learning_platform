from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course

# Create your views here.

@login_required
def course_chat_room(request, course_id):
    """
    Access to course chat-room only for enrolled users.
    Return Course object and 5 Message objects
    """
    try:
        # retrieve course with given id joined by the current user
        course = request.user.course_joined.get(id=course_id)
    except Course.DoesNotExist:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()  # 403
    # retreive chat history; select_related - optimize db queiries
    latest_messages = course.chat_messages.select_related(
        'user'
        ).order_by('-id')[:5]
    latest_messages = reversed(latest_messages)
    return render(request, 
                  'chat/room.html', 
                  {'course': course,
                   'latest_messages': latest_messages})


