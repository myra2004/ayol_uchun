from rest_framework import permissions
from rest_framework.generics import DestroyAPIView

from apps.courses.models import Category


class CategoryDeleteAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)