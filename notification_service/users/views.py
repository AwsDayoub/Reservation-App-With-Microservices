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






def generateRandomNumber():
    l = ['0' , '1' , '2' , '3', '4', '5' , '6' , '7' , '8' , '9']
    random_value = ""
    for _ in range(6):
        random_value += random.choice(l)
    return random_value


def send_verification_email(reciepent , secrete_code):
    context = {
        "secret_code": secrete_code
    }
    sub = "Email Confirmation"
    html_message = render_to_string("users/email_confirmation.html" , context)
    mess = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject= sub,
        body= mess,
        from_email= 'awsdayoub1@gmail.com',
        to= [reciepent]
    )
    message.attach_alternative(html_message , "text/html")
    message.send()
    print("done",reciepent , secrete_code)


class SendEmailAndReceiveVerificationCodeEmail(APIView):
    def get(self , request , email):
        secrete_number = generateRandomNumber()
        send_verification_email(email , secrete_number)
        request.session['sent_value'] = secrete_number
        request.session['sent_time'] = datetime.now().isoformat()
        return Response({'secrete_code': secrete_number} , status=status.HTTP_200_OK)


class SendVerificationCode(APIView):
    serializer_class = SendVerificationCodeSerializer
    def post(self , request):
        if 'sent_value' in request.session and 'sent_time' in request.session:
            sent_value = request.session['sent_value']
            sent_time = datetime.fromisoformat(request.session['sent_time'])
            received_value = request.data['received_value']
            time_difference = abs(datetime.now() - sent_time)
            if sent_value == received_value and time_difference <= timedelta(minutes=5):
                try:
                    user = User.objects.get(username=request.data['username'])
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                user.email_verified = True
                user.save()
                # return 1 if success
                return Response("success")
            else:
                # return 0 if time has expired or value is not correct
                return Response("time has expired or value is not correct")
        else:
            # return -1 if secret code has not sent yet
            return Response("secret code has not sent yet") 


class Register(APIView):
    serializer_class = UserSerializer
    def post(self , request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        secrete_number = generateRandomNumber()
        send_verification_email(request.data['email'] , secrete_number)
        request.session['sent_value'] = secrete_number
        request.session['sent_time'] = datetime.now().isoformat()
        return Response(serializer.data , status=status.HTTP_200_OK)


class LogIn(APIView):
    serializer_class = LoginSerializer
    def post(self , request):
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