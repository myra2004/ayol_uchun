from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.courses.models import Course
from apps.courses.serializers import CourseCreateSerializer


class CourseListAPIVIew(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)