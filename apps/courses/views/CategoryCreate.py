from rest_framework import status, parsers
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.courses.models import Category
from apps.courses.serializers import CategoryCreateSerializer


class CategoryCreatAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)