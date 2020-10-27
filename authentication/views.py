from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from authentication.tasks import post_user,account_activation_mailer
from authentication.serializers import (RegisterSerializer,
                    VerifySerializer,
                    ResendActivationSerializer
                    )
from authentication.service import generate_token
from django.contrib.auth import authenticate
from authentication.models import Otp


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            post_user.delay(user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOtpSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_activation(request):
    serializer = ResendActivationSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.data["email"])
        activaion_mailer.delay(user.id)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.data["email"])
        user_auth = authenticate(username=user.username, password=serializer.data["password"])
        if user_auth:
            post_login(request=request,user=user)
            authenticated = generate_token(user=user)
        return Response(authenticated, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
