from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.users.serializers.PasswordReset import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from apps.users.services.email_send import send_email


class RequestPasswordResetView(APIView):
    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data, context={
            'send_email': send_email
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password reset email sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = []
    @swagger_auto_schema(
        request_body=PasswordResetConfirmSerializer,
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=200)