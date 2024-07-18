from django.shortcuts import render

import random
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP
from .serializers import UserSerializer, OTPSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user, created = User.objects.get_or_create(email=email)
            if created:
                return Response({"message": "Registration successful. Please verify your email."}, status=status.HTTP_201_CREATED)
            return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            OTP.objects.create(user=user, otp=otp)
            print(f"OTP for {email}: {otp}")  # Mock email sending
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_record = OTP.objects.filter(user=user, otp=otp).order_by('-created_at').first()
                if otp_record and (timezone.now() - otp_record.created_at).seconds < 300:  # OTP valid for 5 minutes
                    refresh = RefreshToken.for_user(user)
                    return Response({"message": "Login successful.", "token": str(refresh.access_token)}, status=status.HTTP_200_OK)
                return Response({"message": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
