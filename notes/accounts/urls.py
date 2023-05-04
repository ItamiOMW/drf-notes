from django.urls import path, include

from .views import RegisterAPI, VerifyEmailAPI, ResendVerificationCodeAPI, LoginAPI, LogoutAPI, PasswordResetAPI, PasswordResetConfirmAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('verify-email/', VerifyEmailAPI.as_view()),
    path('verify-email/resend/', ResendVerificationCodeAPI.as_view()),
    path('reset-password/', PasswordResetAPI.as_view()),
    path('reset-password/confirm/', PasswordResetConfirmAPI.as_view()),
]
