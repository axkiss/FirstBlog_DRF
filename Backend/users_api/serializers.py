from django.contrib.auth import get_user_model
from rest_framework import serializers

from users_api.validators import password_validator

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        user = User(username=username)
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email = validated_data['email']
        password_validator(password, user, password2)
        user.set_password(password)
        user.save()
        return user
