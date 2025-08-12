from rest_framework import permissions, status, parsers
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from apps.courses.models import Module
from apps.courses.serializers import ModuleSerializer


class ModuleUpdateAPIView(UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)