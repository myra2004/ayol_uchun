from rest_framework.serializers import ModelSerializer

from apps.courses.models import Webinar


class WebinarCreateSerializer(ModelSerializer):
    class Meta:
        model = Webinar
        fields = [
            'title',
            'description',
            'price',
            'card',
            'category',
            'author',
            'datetime',
            'rating',
        ]