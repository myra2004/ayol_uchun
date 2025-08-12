from rest_framework.serializers import ModelSerializer

from apps.courses.models import Comment


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'course',
            'webinar',
            'text',
            'rating',
        ]

        # read_only_fields = ['user', 'course', 'webinar', 'text', 'rating']