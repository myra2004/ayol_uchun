from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.courses.models import Webinar
from apps.courses.serializers import WebinarCreateSerializer


class WebinarCreatAPIView(CreateAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = WebinarCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)