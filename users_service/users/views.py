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
import random , requests , threading
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
        'http://127.0.0.1:8001/users/signup/',
        'http://127.0.0.1:8002/users/signup/',
        'http://127.0.0.1:8003/users/signup/',
        'http://127.0.0.1:8004/users/signup/',
        'http://127.0.0.1:8005/users/signup/',
        'http://127.0.0.1:8006/users/signup/',
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
        'http://127.0.0.1:8001/users/login/',
        'http://127.0.0.1:8002/users/login/',
        'http://127.0.0.1:8003/users/login/',
        'http://127.0.0.1:8004/users/login/',
        'http://127.0.0.1:8005/users/login/',
        'http://127.0.0.1:8006/users/login/',
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
        'http://127.0.0.1:8001/users/signup/',
        'http://127.0.0.1:8002/users/signup/',
        'http://127.0.0.1:8003/users/signup/',
        'http://127.0.0.1:8004/users/signup/',
        'http://127.0.0.1:8005/users/signup/',
        'http://127.0.0.1:8006/users/signup/',
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
        'http://127.0.0.1:8001/users/logout/',
        'http://127.0.0.1:8002/users/logout/',
        'http://127.0.0.1:8003/users/logout/',
        'http://127.0.0.1:8004/users/logout/',
        'http://127.0.0.1:8005/users/logout/',
        'http://127.0.0.1:8006/users/logout/',
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
        'http://127.0.0.1:8001/users/edit_user_info/',
        'http://127.0.0.1:8002/users/edit_user_info/',
        'http://127.0.0.1:8003/users/edit_user_info/',
        'http://127.0.0.1:8004/users/edit_user_info/',
        'http://127.0.0.1:8005/users/edit_user_info/',
        'http://127.0.0.1:8006/users/edit_user_info/',
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
        'http://127.0.0.1:8001/users/password_reset/',
        'http://127.0.0.1:8002/users/password_reset/',
        'http://127.0.0.1:8003/users/password_reset/',
        'http://127.0.0.1:8004/users/password_reset/',
        'http://127.0.0.1:8005/users/password_reset/',
        'http://127.0.0.1:8006/users/password_reset/',
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
        'http://127.0.0.1:8001/users/delete_user/{username}/',
        'http://127.0.0.1:8002/users/delete_user/{username}/',
        'http://127.0.0.1:8003/users/delete_user/{username}/',
        'http://127.0.0.1:8004/users/delete_user/{username}/',
        'http://127.0.0.1:8005/users/delete_user/{username}/',
        'http://127.0.0.1:8006/users/delete_user/{username}/',
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
    def post(self , request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sendRegisterDataToOtherServices(serializer.data)
        secrete_number = generateRandomNumber()
        send_verification_email(request.data['email'] , secrete_number)
        request.session['sent_value'] = secrete_number
        request.session['sent_time'] = datetime.now().isoformat()
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
                    sendLoginDataToOtherServices({'username':request.data['username'], 'password':request.data['password']})
                    return Response({'message': 'logged in successfuly', 'user_id': user.pk, 'user_type': user.user_type }, status=status.HTTP_200_OK)
                else:
                    sendLoginDataToOtherServices({'username':request.data['username'], 'password':request.data['password']})
                    return Response({'message': 'user already loged in', 'user_id': user.pk, 'user_type': user.user_type }, status=status.HTTP_200_OK)
            else:
                return Response('password not correct' , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('user not found' , status=status.HTTP_404_NOT_FOUND)
        

class LogOut(APIView):
    def post(self , request):
        logout(request)
        sendLogoutDataToOtherServices(request)
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