from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'age', 'country', 'city', 'phone', 'image']


class UpdateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'age', 'country', 'city', 'phone']



class SendVerificationCodeSerializer(serializers.Serializer):
    received_value = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    new_password = serializers.CharField(max_length=128, write_only=True)
