from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer , SendVerificationCodeSerializer , LoginSerializer , ResetPasswordSerializer
from datetime import datetime , timedelta
from .models import User
from django.core.mail import send_mail , EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
import random
# Create your views here.


class Register(APIView):
    serializer_class = UserSerializer
    def post(self , request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)


class LogIn(APIView):
    serializer_class = LoginSerializer
    def post(self , request):
        print(request.data)
        try:
            user = User.objects.get(username=request.data['username'])
        except:
            return Response('user not found' , status=status.HTTP_404_NOT_FOUND)
        if user is not None:
            if user.password == request.data['password']:
                if not user.is_authenticated:
                    login(request , user)
                    return Response({'message': 'logged in successfuly', 'user_id': user.pk, 'user_type': user.user_type }, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'user already loged in', 'user_id': user.pk, 'user_type': user.user_type }, status=status.HTTP_200_OK)
            else:
                return Response('password not correct' , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('user not found' , status=status.HTTP_404_NOT_FOUND)
        

class LogOut(APIView):
    def post(self , request):
        logout(request)
        return Response('user loged out' , status=status.HTTP_200_OK)



class EditUserInfo(APIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    def put(self , request):
        user = User.objects.get(username=request.data['username'])
        print(user)
        if user:
            serializer = UserSerializer(user, data=request.data , partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response("user not found" , status=status.HTTP_404_NOT_FOUND)


class ResetPassword(APIView):
    serializer_class = ResetPasswordSerializer
    def put(self , request):
        try:
            user = User.objects.get(email=request.data['email'])
        except:
            return Response('user not found' , status=status.HTTP_404_NOT_FOUND)
        user.password = request.data['new_password']
        user.save()
        return Response('success' , status=status.HTTP_200_OK)
    

class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, username):
        user = User.objects.get(username=username) 
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)