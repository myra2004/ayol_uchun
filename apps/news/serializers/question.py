from rest_framework import serializers

from apps.news.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'survey',
            'title',
            'type',
            'file',
        ]