from rest_framework import serializers
from courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()


    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses']
