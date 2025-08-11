from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.courses.models import Comment
from apps.courses.serializers import CommentCreateSerializer


class CommentListAPIVIew(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)