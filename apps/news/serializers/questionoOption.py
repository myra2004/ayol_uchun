from rest_framework import serializers

from apps.news.models import QuestionOption


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = [
            'question',
            'title',
        ]