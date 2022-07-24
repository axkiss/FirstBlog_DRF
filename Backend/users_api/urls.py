from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'users_api'

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email_confirm/<uidb64>/<token>/', views.EmailConfirmVerifyView.as_view(), name='email_confirm_verify'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile')
]
