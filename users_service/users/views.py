from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from datetime import datetime , timedelta
from .models import User
from django.core.mail import send_mail , EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import login, logout, authenticate
from drf_spectacular.utils import extend_schema
import random , requests , threading
from rest_framework.authtoken.models import Token
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


# Send Data To Other Services With Multithreading

def sendRegisterDataToOtherServices(data):
    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/signup/',
        'https://awsdayoubcars.pythonanywhere.com/users/signup/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")

    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def sendLoginDataToOtherServices(data):

    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/login/',
        'https://awsdayoubcars.pythonanywhere.com/users/login/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")


    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()

def sendRegisterDataToOtherServices(data):
    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/signup/',
        'https://awsdayoubcars.pythonanywhere.com/users/signup/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")

    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def sendLogoutDataToOtherServices(data):

    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/logout/',
        'https://awsdayoubcars.pythonanywhere.com/users/logout/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")


    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()



def sendEditUserInfoToOtherServices(data):

    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/edit_user_info/',
        'https://awsdayoubcars.pythonanywhere.com/users/edit_user_info/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")


    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()


def sendResetPasswordToOtherServices(data):
    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/password_reset/',
        'https://awsdayoubcars.pythonanywhere.com/users/password_reset/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")

    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()



def sendDeleteUserToOtherServices(data):

    endpoints = [
        'https://awsdayoubhotels.pythonanywhere.com/users/delete_user/{username}/',
        'https://awsdayoubcars.pythonanywhere.com/users/delete_user/{username}/',
    ]

    def send_request(endpoint):
        try:
            response = requests.post(endpoint, data=data)
            print(f"Sent data to {endpoint}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to {endpoint}: {e}")


    threads = []
    for endpoint in endpoints:
        thread = threading.Thread(target=send_request, args=(endpoint,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()



class Register(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sendRegisterDataToOtherServices(serializer.data)
            secret_number = generateRandomNumber()
            send_verification_email(request.data['email'], secret_number)
            request.session['sent_value'] = secret_number
            request.session['sent_time'] = datetime.now().isoformat()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogIn(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data.get('username')
#             password = serializer.validated_data.get('password')

#             try:
#                 user = User.objects.get(username=username)
#                 if user.password == password:
#                     token, created = Token.objects.get_or_create(user=user)
#                     return Response({'token': token.key}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
#             except User.DoesNotExist:
#                 return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogIn(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(username=username)

                # Direct password comparison
                if user.password == password:  # This assumes passwords are not hashed, which is not secure
                    token, created = Token.objects.get_or_create(user=user)

                    # Prepare the user info to be returned
                    user_info = {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'password': user.password,
                        'email': user.email,
                        'age': user.age,
                        'country': user.country,
                        'city': user.city,
                        'phone': user.phone,
                        'balance': user.balance,
                        'user_type': user.user_type,
                    }

                    return Response({'token': token.key, 'user': user_info}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogOut(APIView):
    def post(self , request):
        logout(request)
        sendLogoutDataToOtherServices(request)
        return Response('user loged out' , status=status.HTTP_200_OK)



class EditUserInfo(APIView):
    serializer_class = UpdateInfoSerializer
    #parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated]
    def put(self , request):
        user = User.objects.get(username=request.data['username'])
        print(user)
        if user:
            serializer = UserSerializer(user, data=request.data , partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            sendEditUserInfoToOtherServices(serializer.data)
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
        sendResetPasswordToOtherServices({'email': request.data['email'], 'new_password': request.data['new_password']})
        return Response('success' , status=status.HTTP_200_OK)


class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
            user.delete()
            sendDeleteUserToOtherServices()
            return Response('success', status=status.HTTP_200_OK)
        except:
            return Response('user not found', status=status.HTTP_404_NOT_FOUND)
