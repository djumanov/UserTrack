import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager


class Role(models.Model):
    ADMIN = 1
    EDITOR = 2
    USER = 3
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (USER, 'User'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
      return self.get_id_display()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    roles = models.ManyToManyField(Role)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    email = models.EmailField()
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    sent_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'Email verification for {self.user.email}'


class SMSVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_verifications')
    phone_number = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    sent_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'SMS verification for {self.user.phone_number}'


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    reset_token = models.CharField(max_length=64)
    is_used = models.BooleanField(default=False)
    sent_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Password reset for {self.user.email}'


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'Log: {self.action} by {self.user.username} at {self.timestamp}'
