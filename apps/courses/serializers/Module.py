from rest_framework.serializers import ModelSerializer

from apps.courses.models import Module


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'course',
            'name',
            'icon'
        ]