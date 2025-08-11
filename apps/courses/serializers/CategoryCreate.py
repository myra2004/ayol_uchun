from rest_framework.serializers import ModelSerializer

from apps.courses.models import Category


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'icon',
        ]