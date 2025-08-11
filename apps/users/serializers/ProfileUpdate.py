from rest_framework import serializers

from apps.users.models import User


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            'email',
            'username',
            "avatar",
            "bio",
        ]
        read_only_fields = ["id"]