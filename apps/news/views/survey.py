from rest_framework import status, permissions, parsers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.news.models import Survey
from apps.news.serializers import SurveySerializer


class SurveyListAPIView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SurveyCreateAPIView(CreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAdminUser, ]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser,]

    def post(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyUpdateAPIView(UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class =SurveySerializer
    permission_classes = [permissions.IsAdminUser, ]
    lookup_field = 'id'
    parser_classes = [parsers.FormParser, parsers.MultiPartParser,]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SurveyDeleteAPIView(DestroyAPIView):
    queryset = Survey.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)