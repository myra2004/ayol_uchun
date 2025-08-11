from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.courses.models import Webinar
from apps.courses.serializers import WebinarCreateSerializer


class WebinarListAPIVIew(ListAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarCreateSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)