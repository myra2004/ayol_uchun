from rest_framework import permissions
from rest_framework.generics import DestroyAPIView

from apps.courses.models import Comment


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)