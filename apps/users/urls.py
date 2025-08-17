from django.contrib.auth.views import PasswordResetView
from django.urls import path

from apps.users.views import *


app_name = "users"


urlpatterns = [
    path('registration', RegisterView.as_view(), name='registration'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),

    path('password-reset/request/', RequestPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

    # Profile
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('profile/delete/', ProfileDeleteAPIView.as_view(), name='profile-delete'),
]