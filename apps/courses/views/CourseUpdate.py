from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from apps.courses.models import Course
from apps.courses.serializers import CourseCreateSerializer


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)