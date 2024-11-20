from rest_framework import serializers
from django.db.models import Count
from courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField() # defaults to get_<field_name>

    def get_popular_courses(self, obj):
        courses = obj.courses.annotate(total_students=Count('students')
                                       ).order_by('total_students')[:3]
        return [f'{c.title} ({c.total_students})' for c in courses]


    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 
                  'total_courses', 'popular_courses']
