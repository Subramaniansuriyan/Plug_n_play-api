from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=15,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True,min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'],
            validated_data['password']
        )
        return user

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )

    otp = serializers.CharField(
        required=True,
        min_length=6
    )

    def validate(self,validated_data):
        user = User.objects.filter(email=validated_data["email"])
        otp_data = Otp.objects.filter(user=user.first(),otp=validated_data["otp"],otp_for="ACTIVATION")

        if not user.exists():
            raise serializers.ValidationError({"response":"email_not_found"})
        
        if not otp_data.exists():
            raise serializers.ValidationError({"otp":"Invalid Otp "})
        user.update(is_active=True)
        otp_data.delete()
        return validated_data

class ResendActivationSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
    )

    def validate(self, validated_data):

        user = User.objects.filter(email=validated_data["email"])

        if not user.exists():
            raise serializers.ValidationError({"response":"email_not_found"})
        
        if user.first().is_active:
            raise serializers.ValidationError({"response":"user_active"})

        return validated_data

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
    )
   
    password = serializers.CharField(
        required=True,
        min_length=8
    )

    def validate(self, validated_data):
        user = User.objects.filter(email=validated_data["email"])

        if not user.exists():
            raise serializers.ValidationError({"email":"Email not found."})
        
        if not check_password(validated_data["password"],user.first().password):
            raise serializers.ValidationError({'password':"Password Incorrect"})
        
        if not user.first().is_active:
            raise serializers.ValidationError({"response":"account_not_active"})

        return validated_data