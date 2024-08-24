from django.shortcuts import render , get_object_or_404
from django.db.models import Q , F , Prefetch
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from datetime import datetime
from dateutil.parser import parse
from .models import *
from .serializer import *
from .paginations import CarCompanyListPagination , CityListPagination
from .permissions import IsManager
from .tasks import change_car_status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
import requests
# Create your views here.


class SearchForCarCompanies(generics.ListAPIView):
    serializer_class = CarCompanySerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        word = self.kwargs.get('word', '')
        queryset = CarCompany.objects.filter(
            Q(name__icontains=word) |
            Q(city__name__icontains=word) |
            Q(country__icontains=word)
        )
        return queryset


class ShowCarCompanies(generics.ListAPIView):
    queryset = CarCompany.objects.annotate(rate=F('sum_of_rates') / F('number_of_rates')).order_by('rate', '-date_created')
    serializer_class = CarCompanySerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CarCompanyListPagination

class ShowCities(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
   # permission_classes = [IsAuthenticated]
 #   throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CityListPagination

class ShowCityCarCompanies(APIView):
    serializer_class = CarCompanySerializer
   # permission_classes = [IsAuthenticated]
   # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CarCompanyListPagination
    def get(self, request, city_id):
        hotels = CarCompany.objects.filter(city=city_id)
        serializer = self.serializer_class(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ShowCityCarCompanies(APIView):
    serializer_class = CarCompanySerializer
   # permission_classes = [IsAuthenticated]
   # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CarCompanyListPagination
    def get(self, request, city_id):
        hotels = CarCompany.objects.filter(city=city_id)
        serializer = self.serializer_class(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowCarCompanyDetails(APIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = CarCompanyWithImagesSerializer
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, car_company_id):
        car_company = get_object_or_404(CarCompany, pk=car_company_id)
        images = CarCompanyImages.objects.filter(car_company=car_company_id)
        car_company.images = images
        serializer = self.serializer_class(car_company)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ShowCars(APIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = CarWithCarImagesSerializer
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self , request , car_company_id):
        cars = Car.objects.filter(car_company_id=car_company_id , reserved=False)
        for car in cars:
            images = CarImages.objects.filter(car=car.pk)
            car.images = images
        serializer = CarWithCarImagesSerializer(cars , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class ShowCarDetails(APIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = CarWithCarImagesSerializer
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        images = CarImages.objects.filter(car=car_id)
        car.images = images
        serializer = self.serializer_class(car)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ShowCarReservationDetails(APIView):
    #permission_classes = [IsAuthenticated , IsManager]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CarReservationWithIdImageSerializer

    def get(self , request , car_id):
        reservation = get_object_or_404(CarReservation , car_id=car_id)
        images =  CarReservationIdImage.objects.filter(reservation_id=reservation.pk)
        reservation.images = images
        serializer = self.serializer_class(reservation)
        return Response(serializer.data , status=status.HTTP_200_OK)

class ShowCarCompanyReservationsDetails(APIView):
    #permission_classes = [IsAuthenticated , IsManager]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CarReservationWithIdImageSerializer

    def get(self , request , car_company_id):
        reservations = CarReservation.objects.filter(car_company_id=car_company_id)
        for reservation in reservations:
            images =  CarReservationIdImage.objects.filter(reservation_id=reservation.pk)
            reservation.images = images
        serializer = self.serializer_class(reservations , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ShowCarCompanyComments(generics.ListAPIView):
    #permission_classes = [IsAuthenticated , IsManager]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CarCompanyCommentsSerializer
    def get_queryset(self):
        car_company_id = self.kwargs.get('car_company_id')
        return CarCompanyComments.objects.filter(car_company_id=car_company_id)


class AddCarCompany(APIView):
    serializer_class = CarCompanySerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated , IsManager]
    #throttle_classes = [AnonRateThrottle , UserRateThrottle]
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'object created, use the returned id to post images for it', 'id': serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddCarCompanyImage(generics.CreateAPIView):
    serializer_class = CarCompanyImageSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated, IsManager]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]

class AddCar(generics.CreateAPIView):
    serializer_class = CarSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated , IsManager]
    #throttle_classes = [AnonRateThrottle , UserRateThrottle]
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'object created, use the returned id to post images for it', 'id': serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCarImages(generics.CreateAPIView):
    serializer_class = CarImagesSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated, IsManager]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]



# class AddCarReservation(APIView):
#     serializer_class = CarReservationSerializer
#     #permission_classes = [IsAuthenticated]
#     #throttle_classes = [AnonRateThrottle , UserRateThrottle]
#     def post(self, request , car_id):
#         car = Car.objects.get(id=car_id)
#         if request.user.balance < car.price:
#             return Response('not enouph balance' , status=status.HTTP_400_BAD_REQUEST)
#         elif car.reserved:
#             return Response('car already reserved', status=status.HTTP_400_BAD_REQUEST)
#         else:
#             car.reserved = True
#             car.save()
#             serializer = self.serializer_class(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 # schedule task to change car status
#                 #change_car_status.apply_async(args=[car_id], eta=serializer.data['end_date'])
#                 end_date = parse(serializer.data['end_date']).replace(tzinfo=None)
#                 countdown = (end_date - datetime.now()).total_seconds()
#                 # Ensure countdown is not negative
#                 countdown = max(countdown, 0)
#                 # Schedule task to change car status
#                 #change_car_status.apply_async(args=[car_id], countdown=countdown)
#                 return Response({'reservation_id': serializer.data.get('pk')}, status=status.HTTP_200_OK)
#             else:
#                 return Response('not valid data', status=status.HTTP_400_BAD_REQUEST)

def send_reservation_email(user_email, car_details):
    subject = 'Your Car Reservation Confirmation'
    message = f'''
    Dear Customer,

    Your reservation has been confirmed.

    Car Details:
    - Car ID: {car_details['car_id']}
    - Car Type: {car_details['car_type']}
    - Price: ${car_details['price']}
    - Description: {car_details['description']}

    Thank you for booking with us!

    Best regards
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)


# class ReserveCarView(APIView):
#     serializer_class = CarReservationSerializer
#     def post(self, request):

#         input_serializer = CarReservationSerializer(data=request.data)
#         if not input_serializer.is_valid():
#             return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         user_id = input_serializer.validated_data.get('user_id')
#         car_id = input_serializer.validated_data.get('car_id')


#         car = get_object_or_404(Car, id=car_id)


#         user = get_object_or_404(User, id=user_id)


#         if user.balance < car.price:
#             return Response({'detail': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)


#         user.balance -= car.price
#         user.save()



#         car_details = {
#             'car_id': car.id,
#             'car_type': car.car_type,
#             'price': car.price,
#             'description': car.description,
#         }

#         send_reservation_email(user.email, car_details)


#         car_serializer = CarSerializer(car)
#         return Response(car_serializer.data, status=status.HTTP_200_OK)
class ReserveCarView(APIView):
    serializer_class = CarReservationPostSerializer

    def post(self, request):
        input_serializer = CarReservationPostSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Correct usage: Getting the IDs from the validated data
        username = input_serializer.validated_data.get('username')
        car_id = input_serializer.validated_data.get('car_id')
        car_company_id = input_serializer.validated_data.get('car_company_id')

        # Fetching objects using the IDs
        try:
            car = Car.objects.get(id=car_id)
        except:
            return Response({'detail': 'car not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except:
            return Response({'detail': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car_company = CarCompany.objects.get(id=car_company_id)
        except:
            return Response({'detail': 'car company not found'}, status=status.HTTP_400_BAD_REQUEST)

        # car = get_object_or_404(Car, id=car_id)
        # user = get_object_or_404(User, username=username)
        # car_company = get_object_or_404(CarCompany, id=car_company_id)

        # Check balance and reserve the car
        if user.balance < car.price:
            return Response({'detail': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        user.balance -= car.price
        user.save()



        url = "https://awsdayoubhotels.pythonanywhere.com/hotel/update_balance/"
        data = {
            "username": user.username,
            "balance": int(user.balance)
        }

        response = requests.put(url, json=data)

        #car.reserved = True
        car.save()

        # Create the car reservation
        car_reservation = CarReservation.objects.create(
            car_company=car_company,
            car=car,
            user=user,
            start_date=input_serializer.validated_data.get('start_date'),
            end_date=input_serializer.validated_data.get('end_date'),
            pickup_location=input_serializer.validated_data.get('pickup_location'),
            delivery_location=input_serializer.validated_data.get('delivery_location'),
            description=input_serializer.validated_data.get('description'),
        )

        car_details = {
            'car_id': car.id,
            'car_type': car.car_type,
            'price': car.price,
            'description': car.description,
        }

        send_reservation_email(user.email, car_details)

        return Response({'balance': int(user.balance)}, status=status.HTTP_200_OK)


class AddCarReservationIDImage(generics.CreateAPIView):
    serializer_class = CarReservationIdImageSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]



class AddCarCompanyComment(generics.CreateAPIView):
    serializer_class = CarCompanyCommentsSerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [AnonRateThrottle, UserRateThrottle]



class UpdateCarCompany(APIView):
    serializer_class = CarCompanySerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated , IsManager]
    def put(self , request):
        try:
            carcompany = CarCompany.objects.get(id=request.data['id'])
        except CarCompany.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(carcompany, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateCar(APIView):
    serializer_class = CarSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated , IsManager]
    def put(self , request):
        try:
            car = Car.objects.get(id=request.data['id'])
        except Car.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateComment(APIView):
    serializer_class = CarCompanyCommentsSerializer
    #permission_classes = [IsAuthenticated]
    def put(self , request):
        try:
            comment = CarCompanyComments.objects.get(id=request.data['id'])
        except CarCompanyComments.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCarCompanyImage(APIView):
    #permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_company_image_id):
        try:
            image = CarCompanyImages.objects.get(id=car_company_image_id)
        except CarCompanyImages.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response('success', status=status.HTTP_200_OK)


class DeleteCarImage(APIView):
    #permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_image_id):
        try:
            image = CarImages.objects.get(id=car_image_id)
        except CarImages.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response('success', status=status.HTTP_200_OK)



class DeleteCarCompany(APIView):
   #permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_company_id):
        try:
            carcompany = CarCompany.objects.get(id=car_company_id)
        except CarCompany.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        carcompany.delete()
        return Response('success', status=status.HTTP_200_OK)




class DeleteCar(APIView):
    #permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        car.delete()
        return Response('success', status=status.HTTP_200_OK)


class DeleteCarCompanyComment(APIView):
    #permission_classes = [IsAuthenticated]
    def delete(self , request , car_company_comment_id):
        try:
            carcompanycomment = CarCompanyComments.objects.get(id=car_company_comment_id)
        except CarCompanyComments.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        carcompanycomment.delete()
        return Response('success', status=status.HTTP_200_OK)




class ShowCustomerReservations(APIView):
    serializer_class = CarReservationSerializer
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        reservations = CarReservation.objects.filter(user=user.id)
        # carcompany = CarCompany.objects.get(id=reservations['car_company_id'])
        serializer = self.serializer_class(reservations, many=True)
        # serializer["car_company_name"] = carcompany.name
        return Response(serializer.data, status=status.HTTP_200_OK)




class UpdateBalance(APIView):
    serializer_class = BalanceSerializer
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            balance = serializer.validated_data['balance']
        user = User.object.get(username=username)
        user.balance = balance
        user.save()
        return Response('success' , status=status.HTTP_200_OK)


