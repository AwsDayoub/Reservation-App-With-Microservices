from django.shortcuts import render
from django.db.models import Q , F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from .paginations import HotelListPagination, CityListPagination
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permissions import IsManager
from rest_framework import generics
from django.shortcuts import get_object_or_404
from users.models import User
from django.conf import settings
from django.core.mail import send_mail
import random , requests , threading
# Create your views here.


class SearchForHotels(generics.ListAPIView):
    serializer_class = HotelSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        word = self.kwargs.get('word', '')
        queryset = Hotel.objects.filter(
            Q(name__icontains=word) |
            Q(city__name__icontains=word) |
            Q(country__icontains=word)
        )
        return queryset

class ShowHotels(generics.ListAPIView):
    queryset = Hotel.objects.annotate(rate=F('sum_of_rates') / F('number_of_rates')).order_by('rate', '-date_created')
    serializer_class = HotelSerializer
  #  permission_classes = [IsAuthenticated]
   # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = HotelListPagination



class ShowCities(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
   # permission_classes = [IsAuthenticated]
 #   throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CityListPagination



class ShowCityHotels(APIView):
    serializer_class = HotelSerializer
   # permission_classes = [IsAuthenticated]
   # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = HotelListPagination
    def get(self, request, city_id):
        hotels = Hotel.objects.filter(city=city_id)
        serializer = self.serializer_class(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowHotelDetails(APIView):
    serializer_class = HotelSerializer
  #  permission_classes = [IsAuthenticated]
  #  throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        hotel = Hotel.objects.get(pk=hotel_id)
        serializer = self.serializer_class(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowHotelStays(APIView):
    serializer_class = StaySerializer
  # permission_classes = [IsAuthenticated]
   # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        stays = Stay.objects.filter(hotel_id=hotel_id)
        serializer = self.serializer_class(stays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowHotelImages(APIView):
    serializer_class = HotelImagesSerializer
   # permission_classes = [IsAuthenticated]
  #  throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        images = HotelImages.objects.filter(hotel=hotel_id)
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ShowHotelFeatures(APIView):
    serializer_class = HotelFeaturesSerializer
   # permission_classes = [IsAuthenticated]
  #  throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        features = Features.objects.filter(hotel=hotel_id)
        serializer = self.serializer_class(features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ShowHotelComments(APIView):
    serializer_class = HotelCommentsSerializer
 #   permission_classes = [IsAuthenticated]
   # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        comments = HotelComments.objects.filter(hotel_id=hotel_id)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_reservation_email(user_email, stay_details):
    subject = 'Your Stay Reservation Confirmation'
    message = f'''
    Dear Customer,

    Your reservation has been confirmed.

    Stay Details:
    - Hotel Name: {stay_details['hotel_name']}
    - Stay Type: {stay_details['stay_type']}
    - Price: ${stay_details['price']}
    - Description: {stay_details['description']}

    Thank you for booking with us!

    Best regards,
    The Hotel Team
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)

def sendBalanceDataToOtherServices(data):
    endpoints = [
        'https://awsdayoubcars.pythonanywhere.com/carcompany/update_balance/',
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

class ReserveStayView(APIView):
    serializer_class = ReservationPostSerializer

    def post(self, request):
        # Directly get the values from request.data
        username = request.data.get('username')
        stay_id = request.data.get('stay_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        note = request.data.get('note', '')

        # Validate the required fields
        if not all([username, stay_id, start_date, end_date]):
            return Response({'detail': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Stay object, raising 404 if not found
        # stay = get_object_or_404(Stay, id=stay_id)

        try:
            stay = Stay.objects.get(id=stay_id)
        except:
            return Response({'detail': 'stay not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except:
            return Response({'detail': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the User object, raising 404 if not found
        # user = get_object_or_404(User, username=username)

        # Check if the user has enough balance
        if user.balance < stay.price:
            return Response({'detail': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct balance and save the user
        user.balance -= stay.price
        user.save()



        # url = "https://awsdayoubcars.pythonanywhere.com/carcompany/update_balance/"
        data = {
            "username": user.username,
            "balance": int(user.balance)
        }

        # response = requests.post(url, json=data)

        sendBalanceDataToOtherServices(data)

        # Create the HotelReservation object
        hotel_reservation = HotelReservation.objects.create(
            hotel_id=stay.hotel_id,
            stay_id=stay,
            user_id=user,
            start_date=start_date,
            end_date=end_date,
            note=note
        )

        # Prepare and send the reservation email
        stay_details = {
            'hotel_name': stay.hotel_id.name,
            'stay_type': stay.stay_type,
            'price': stay.price,
            'description': stay.description,
        }
        send_reservation_email(user.email, stay_details)

        # Serialize the Stay object and return the response
        stay_serializer = StaySerializer(stay)
        return Response({'balance': int(user.balance)}, status=status.HTTP_200_OK)


class ShowCustomerReservations(APIView):
    serializer_class = ReservationSerializer
    def get(self, request, username):
        user = get_object_or_404(User,username=username)
        reservations = HotelReservation.objects.filter(user_id=user.id)
        serializer = self.serializer_class(reservations, many=True)
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

