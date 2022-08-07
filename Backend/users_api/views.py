from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users_api.models import ExtraUserProfile
from users_api.serializers import MyTokenObtainPairSerializer, RegisterUserSerializer, UserProfileSerializer
from users_api.services import get_user_by_uidb, check_user_and_token, add_user_to_group
from users_api.utils import send_email_for_verify

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom login view"""
    serializer_class = MyTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Show user profile"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

    def get_permissions(self):
        match self.request.method:
            case 'GET':
                permission_classes = [permissions.IsAuthenticated]
            case 'PUT' | 'PATCH':
                if self.request.user.username == self.kwargs.get('username'):
                    permission_classes = [permissions.AllowAny]
                else:
                    permission_classes = [permissions.IsAdminUser]
            case _:
                permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]


class RegisterView(generics.GenericAPIView):
    """Register and send email for verify new user"""
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_email_for_verify(self.request, user)
        return Response({
            "message": "The user has been successfully created."
                       "Please, check your email and confirm email for complete registration."})


class EmailConfirmVerifyView(generics.GenericAPIView):
    """Confirm user email or show message about an invalid link """
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        user = get_user_by_uidb(uidb64)
        if check_user_and_token(user, token):
            user.email_verify = True
            user.save()
            add_user_to_group(user, group_name='Reader')
            ExtraUserProfile.objects.get_or_create(user=user)
            return Response({"message": "Email confirm."})
        return Response({"message": "Email invalid confirm. Link is incorrect."})
