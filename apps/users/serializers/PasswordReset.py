from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import User
from apps.users.services.tokens import generate_email_confirm_token, verify_email_confirm_token


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return value

    def save(self):
        # token = generate_password_reset_token(self.user)
        # send_email_task = self.context['send_email'](self.user, token)
        # send_email_task.delay()
        token = generate_email_confirm_token(self.user)
        # user_id = self.user.id
        # self.context['send_email'].delay(user_id, token)
        self.context['send_email'](
            subject = 'Reset Your Password',
            intro_text = 'Please confirm your email address',
            email = self.email,
            token = token,
            template = 'reset_password_email.html'
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_id = verify_email_confirm_token(attrs["token"])
        if not user_id:
            raise serializers.ValidationError("Invalid or expired token.")
        self.user = User.objects.get(pk=user_id)
        validate_password(attrs["new_password"], self.user)
        return attrs

    def save(self):
        self.user.set_password(self.validated_data["new_password"])
        self.user.save()