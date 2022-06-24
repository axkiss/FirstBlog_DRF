from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
]