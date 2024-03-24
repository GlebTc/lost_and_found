from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role', 'id', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Custom logic for creating a user
        user = CustomUser.objects.create_user(**validated_data)
        return user