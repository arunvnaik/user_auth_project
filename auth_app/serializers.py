from rest_framework import serializers
from .models import User, OTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'otp', 'otp_created_at']  # Include 'otp' and 'otp_created_at' if needed

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user', 'otp', 'created_at']
