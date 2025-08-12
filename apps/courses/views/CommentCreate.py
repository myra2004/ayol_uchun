from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.courses.models import Comment
from apps.courses.serializers import CommentCreateSerializer


class CommentCreatAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)