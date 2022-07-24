from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users_api.utils import send_email_for_verify
from users_api.validators import password_validator

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for check email verify when user logining"""

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        if not self.user.email_verify and not self.user.is_superuser:
            send_email_for_verify(self.context["request"], self.user)
            raise exceptions.AuthenticationFailed(
                _("Email is not verify, check your email."),
                "no_email_verify",
            )
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'groups')


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
