from rest_framework.serializers import ModelSerializer

from apps.courses.models import Course


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'price',
            'card',
            'category',
            'author',
            'rating',
        ]