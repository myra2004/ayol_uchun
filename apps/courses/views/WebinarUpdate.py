from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from apps.courses.models import Webinar
from apps.courses.serializers import WebinarCreateSerializer


class WebinarUpdateAPIView(UpdateAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarCreateSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)