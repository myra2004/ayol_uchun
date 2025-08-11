from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import User
from core import settings
from apps.users.services.tokens import *


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("Email is already in use")
        return value


    def create(self, validated_data):
        print(">>>", validated_data.get("email"))
        email = validated_data.get("email")
        password = make_password(validated_data.get("password"))

        user = User.objects.filter(email=email, is_active=False).first()
        if user:
            user.password = password
            user.save()
        else:
            user = User.objects._create_user(email=email, password=password)
            user.is_active = False
            user.save()

        token = generate_email_confirm_token(user)

        self.context['send_email'](
            subject = 'Create Your account',
            intro_text='Click the link below to create your account.',
            email=email,
            template='send_verify_email.html',
            token=token,
            password=password,
        )

        return user


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        user_id = verify_email_confirm_token(attrs["token"])
        print(">>>", user_id)
        if not user_id:
            raise serializers.ValidationError("Invalid or expired token.")
        self.user = User.objects.get(pk=user_id)
        validate_password(attrs["new_password"], self.user)
        return attrs

    def save(self):
        self.user.is_active = True
        self.user.set_password(self.validated_data["new_password"])
        self.user.save()
