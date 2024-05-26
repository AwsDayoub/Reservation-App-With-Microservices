from django.shortcuts import render
from django.db.models import Q , F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, City , HotelImages, Features, Stay, StayImages, HotelComments
from .serializer import HotelSerializer, CitySerializer, HotelBigSerializer, StaySerializer , HotelImagesSerializer, HotelFeaturesSerializer, HotelCommentsSerializer
from .paginations import HotelListPagination, CityListPagination
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permissions import IsManager
from rest_framework import generics
# Create your views here.


class SearchForHotels(generics.ListAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        word = self.kwargs.get('word', '')
        queryset = Hotel.objects.filter(
            Q(name__icontains=word) |
            Q(city__icontains=word) |
            Q(country__icontains=word)
        )
        return queryset


class ShowHotels(generics.ListAPIView):
    queryset = Hotel.objects.annotate(rate=F('sum_of_rates') / F('number_of_rates')).order_by('rate', '-date_created')
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = HotelListPagination



class ShowCities(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CityListPagination 



class ShowCityHotels(APIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = HotelListPagination
    def get(self, request, city_id):
        hotels = Hotel.objects.filter(city=city_id)
        serializer = self.serializer_class(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowHotelDetails(APIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        hotel = Hotel.objects.get(pk=hotel_id)
        serializer = self.serializer_class(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowHotelStays(APIView):
    serializer_class = StaySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        stays = Stay.objects.filter(hotel_id=hotel_id)
        serializer = self.serializer_class(stays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ShowHotelImages(APIView):
    serializer_class = HotelImagesSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        images = HotelImages.objects.filter(hotel=hotel_id)
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ShowHotelFeatures(APIView):
    serializer_class = HotelFeaturesSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        features = Features.objects.filter(hotel=hotel_id)
        serializer = self.serializer_class(features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ShowHotelComments(APIView):
    serializer_class = HotelCommentsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, hotel_id):
        comments = HotelComments.objects.filter(hotel_id=hotel_id)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    