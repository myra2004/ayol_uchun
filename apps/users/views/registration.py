from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.services.email_send import send_code
from apps.users.serializers.Registration import RegisterSerializer, VerifyCodeSerializer


class RegisterView(APIView):
    permission_classes = []
    @swagger_auto_schema(
        request_body=RegisterSerializer
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={
            'send_code': send_code
        })
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Verification code sent. Please check your inbox."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=VerifyCodeSerializer,
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Account is created succesfully."}, status=200)
