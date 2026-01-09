from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
    TwoFactorVerifySerializer
)
from .services import TwoFactorService, EmailService


class UserRegistrationView(generics.CreateAPIView):
    """API view for user registration."""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification email
        email_service = EmailService()
        # In production, generate actual verification URL
        verification_url = f"{request.build_absolute_uri('/auth/verify-email/')}?token=..."
        email_service.send_verification_email(user, verification_url)
        email_service.send_welcome_email(user)
        
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Registration successful. Please check your email to verify your account.'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """API view for user login."""
    
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(csrf_protect)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Check if 2FA is enabled
        if user.is_2fa_enabled:
            # Return temporary token for 2FA verification
            return Response({
                'requires_2fa': True,
                'message': 'Please enter your 2FA code.',
                'temp_token': Token.objects.get_or_create(user=user)[0].key
            }, status=status.HTTP_200_OK)
        
        # Login user
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """API view for user logout."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Delete user token
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        logout(request)
        
        return Response({
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API view for user profile."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Update user fields
        user_serializer = self.get_serializer(instance, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        
        # Update profile fields
        profile_data = {k: v for k, v in request.data.items() 
                       if k in ['bio', 'avatar', 'date_of_birth', 'address', 
                               'city', 'country', 'postal_code', 'website', 
                               'twitter', 'linkedin', 'github']}
        
        if profile_data:
            profile_serializer = UserProfileSerializer(
                instance.profile, 
                data=profile_data, 
                partial=True
            )
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
        
        return Response(UserSerializer(instance).data)


class PasswordChangeView(APIView):
    """API view for password change."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Update token
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Password changed successfully.',
            'token': token.key
        }, status=status.HTTP_200_OK)


class Enable2FAView(APIView):
    """API view to enable 2FA."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if user.is_2fa_enabled:
            return Response({
                'message': '2FA is already enabled.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        service = TwoFactorService()
        result = service.enable_2fa(user)
        
        # Convert QR code to base64 for response
        import base64
        qr_code_base64 = base64.b64encode(result['qr_code']).decode('utf-8')
        
        return Response({
            'message': 'Scan the QR code with your authenticator app.',
            'qr_code': f'data:image/png;base64,{qr_code_base64}',
            'secret_key': result['secret_key'],
            'backup_codes': result['backup_codes']
        }, status=status.HTTP_200_OK)


class Verify2FAView(APIView):
    """API view to verify 2FA token."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        token = serializer.validated_data['token']
        
        service = TwoFactorService()
        is_valid = service.verify_2fa_token(user, token)
        
        if is_valid:
            # Send confirmation email
            email_service = EmailService()
            email_service.send_2fa_enabled_email(user)
            
            return Response({
                'message': '2FA verified and enabled successfully.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Invalid 2FA token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class Disable2FAView(APIView):
    """API view to disable 2FA."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if not user.is_2fa_enabled:
            return Response({
                'message': '2FA is not enabled.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        service = TwoFactorService()
        service.disable_2fa(user)
        
        return Response({
            'message': '2FA disabled successfully.'
        }, status=status.HTTP_200_OK)


class RegenerateBackupCodesView(APIView):
    """API view to regenerate 2FA backup codes."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if not user.is_2fa_enabled:
            return Response({
                'message': '2FA is not enabled.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        service = TwoFactorService()
        backup_codes = service.generate_backup_codes(user)
        
        return Response({
            'message': 'Backup codes regenerated successfully.',
            'backup_codes': backup_codes
        }, status=status.HTTP_200_OK)
