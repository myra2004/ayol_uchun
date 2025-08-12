from rest_framework import permissions
from rest_framework.generics import DestroyAPIView

from apps.courses.models import Module


class ModuleDeleteAPIView(DestroyAPIView):
    queryset = Module.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)