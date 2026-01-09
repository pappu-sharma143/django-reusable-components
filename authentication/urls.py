from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    PasswordChangeView,
    Enable2FAView,
    Verify2FAView,
    Disable2FAView,
    RegenerateBackupCodesView
)

app_name = 'authentication'

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    
    # Two-Factor Authentication
    path('2fa/enable/', Enable2FAView.as_view(), name='2fa-enable'),
    path('2fa/verify/', Verify2FAView.as_view(), name='2fa-verify'),
    path('2fa/disable/', Disable2FAView.as_view(), name='2fa-disable'),
    path('2fa/backup-codes/', RegenerateBackupCodesView.as_view(), name='2fa-backup-codes'),
]
