from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # empty queryset - avoids unnecessary db load during from init-tion
    course = forms.ModelChoiceField(queryset=Course.objects.none(),
                                    widget=forms.HiddenInput)
    
    # populate queryset
    def __init__(self, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()