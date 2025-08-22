from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import User
from apps.users.services.tokens import *


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value, username=value, is_active=True).exists():
            raise serializers.ValidationError("Phone Number is already in use")
        return value


    def create(self, validated_data):
        print(">>>", validated_data.get("phone_number"))
        phone_number = validated_data.get("phone_number")
        username = validated_data.get("username")
        password = make_password(validated_data.get("password"))

        user = User.objects.filter(phone_number=phone_number, username=username, is_active=False).first()
        if user:
            user.password = password
            user.save()
        else:
            user = User.objects._create_user(phone_number=phone_number, username=username, password=password)
            user.is_active = False
            user.save()

        token = generate_number_confirm_token(user)

        self.context['send_code'](
            subject = 'Create Your account',
            intro_text='Click the link below to create your account.',
            phone_number=phone_number,
            username=username,
            template='send_verify_number.html',
            token=token,
            password=password,
        )

        return user


class VerifyCodeSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        user_id = verify_number_confirm_token(attrs["token"])
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
