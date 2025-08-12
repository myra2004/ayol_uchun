from rest_framework import serializers

from apps.news.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = [
            'course',
            'title',
            'description',
            'card',
        ]