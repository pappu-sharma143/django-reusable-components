import secrets
import qrcode
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import TwoFactorBackupCode, User


class TwoFactorService:
    """Service for handling two-factor authentication operations."""
    
    def enable_2fa(self, user):
        """
        Enable 2FA for a user and generate QR code.
        
        Args:
            user: User instance
            
        Returns:
            dict: Contains QR code data URL and secret key
        """
        # Create or get TOTP device
        device, created = TOTPDevice.objects.get_or_create(
            user=user,
            name='default',
            confirmed=False
        )
        
        # Generate QR code
        qr_url = device.config_url
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_data = buffer.getvalue()
        
        # Generate backup codes
        backup_codes = self.generate_backup_codes(user)
        
        return {
            'qr_code': qr_code_data,
            'secret_key': device.key,
            'backup_codes': backup_codes
        }
    
    def verify_2fa_token(self, user, token):
        """
        Verify a 2FA token for a user.
        
        Args:
            user: User instance
            token: 6-digit TOTP token
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            device = TOTPDevice.objects.get(user=user, name='default')
            
            # Verify token
            if device.verify_token(token):
                if not device.confirmed:
                    device.confirmed = True
                    device.save()
                    user.is_2fa_enabled = True
                    user.save()
                return True
            
            # Check backup codes if token verification fails
            return self._verify_backup_code(user, token)
            
        except TOTPDevice.DoesNotExist:
            return False
    
    def disable_2fa(self, user):
        """
        Disable 2FA for a user.
        
        Args:
            user: User instance
        """
        TOTPDevice.objects.filter(user=user).delete()
        TwoFactorBackupCode.objects.filter(user=user).delete()
        user.is_2fa_enabled = False
        user.save()
    
    def generate_backup_codes(self, user, count=10):
        """
        Generate backup codes for 2FA recovery.
        
        Args:
            user: User instance
            count: Number of backup codes to generate
            
        Returns:
            list: List of backup codes
        """
        # Delete existing backup codes
        TwoFactorBackupCode.objects.filter(user=user).delete()
        
        codes = []
        for _ in range(count):
            code = secrets.token_hex(5).upper()  # 10-character code
            TwoFactorBackupCode.objects.create(user=user, code=code)
            codes.append(code)
        
        return codes
    
    def _verify_backup_code(self, user, code):
        """
        Verify a backup code.
        
        Args:
            user: User instance
            code: Backup code
            
        Returns:
            bool: True if code is valid, False otherwise
        """
        try:
            backup_code = TwoFactorBackupCode.objects.get(
                user=user,
                code=code.upper(),
                is_used=False
            )
            backup_code.mark_as_used()
            return True
        except TwoFactorBackupCode.DoesNotExist:
            return False


class EmailService:
    """Service for handling email operations."""
    
    def send_verification_email(self, user, verification_url):
        """
        Send email verification to user.
        
        Args:
            user: User instance
            verification_url: URL for email verification
        """
        subject = 'Verify Your Email Address'
        context = {
            'user': user,
            'verification_url': verification_url,
        }
        
        html_message = render_to_string('authentication/emails/verify_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    def send_password_reset_email(self, user, reset_url):
        """
        Send password reset email to user.
        
        Args:
            user: User instance
            reset_url: URL for password reset
        """
        subject = 'Reset Your Password'
        context = {
            'user': user,
            'reset_url': reset_url,
        }
        
        html_message = render_to_string('authentication/emails/password_reset.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    def send_welcome_email(self, user):
        """
        Send welcome email to new user.
        
        Args:
            user: User instance
        """
        subject = 'Welcome to Our Platform!'
        context = {
            'user': user,
        }
        
        html_message = render_to_string('authentication/emails/welcome.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    def send_2fa_enabled_email(self, user):
        """
        Send notification when 2FA is enabled.
        
        Args:
            user: User instance
        """
        subject = 'Two-Factor Authentication Enabled'
        context = {
            'user': user,
        }
        
        html_message = render_to_string('authentication/emails/2fa_enabled.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
