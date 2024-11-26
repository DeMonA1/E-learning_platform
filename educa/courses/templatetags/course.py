from django import template


register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
    
@register.filter
def user_is_instructor(obj):
    # obj = request
    try:
        return obj.user.groups.filter(name='Instructors').exists()
    except AttributeError:
        None