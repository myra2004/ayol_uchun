from rest_framework.serializers import ModelSerializer

from apps.courses.models import Lesson


class LessonCreateSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'module',
            'title',
            'description',
            'file',
            'duration'
        ]