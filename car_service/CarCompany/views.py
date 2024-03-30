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
from .models import *
from .serializer import *
from .paginations import CarCompanyListPagination
from .permissions import IsManager


# Create your views here.


class SearchForCarCompanies(generics.ListAPIView):
    serializer_class = CarCompanySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        word = self.kwargs.get('word', '')
        queryset = CarCompany.objects.filter(
            Q(name__icontains=word) |
            Q(city__icontains=word) |
            Q(country__icontains=word)
        )
        return queryset


class ShowCarCompanies(generics.ListAPIView):
    queryset = CarCompany.objects.annotate(rate=F('sum_of_rates') / F('number_of_rates')).order_by('rate', '-date_created')
    serializer_class = CarCompanySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CarCompanyListPagination




class ShowCarCompanyDetails(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarCompanyWithImagesSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, car_company_id):
        car_company = get_object_or_404(CarCompany, pk=car_company_id)
        images = CarCompanyImages.objects.filter(car_company=car_company_id)
        car_company.images = images
        serializer = self.serializer_class(car_company)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ShowCars(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarWithCarImagesSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self , request , car_company_id):
        cars = Car.objects.filter(car_company_id=car_company_id , reserved=False)
        for car in cars:
            images = CarImages.objects.filter(car=car.pk)
            car.images = images
        serializer = CarWithCarImagesSerializer(cars , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class ShowCarDetails(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarWithCarImagesSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        images = CarImages.objects.filter(car=car_id)
        car.images = images
        serializer = self.serializer_class(car)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ShowCarReservationDetails(APIView):
    permission_classes = [IsAuthenticated , IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CarReservationWithIdImageSerializer

    def get(self , request , car_id):
        reservation = get_object_or_404(CarReservation , car_id=car_id)
        images =  CarReservationIdImage.objects.filter(reservation_id=reservation.pk)
        reservation.images = images
        serializer = self.serializer_class(reservation)
        return Response(serializer.data , status=status.HTTP_200_OK)

class ShowCarCompanyReservationsDetails(APIView):
    permission_classes = [IsAuthenticated , IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CarReservationWithIdImageSerializer

    def get(self , request , car_company_id):
        reservations = CarReservation.objects.filter(car_company_id=car_company_id)
        for reservation in reservations:
            images =  CarReservationIdImage.objects.filter(reservation_id=reservation.pk)
            reservation.images = images
        serializer = self.serializer_class(reservations , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ShowCarCompanyComments(generics.ListAPIView):
    permission_classes = [IsAuthenticated , IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CarCompanyCommentsSerializer
    def get_queryset(self):
        car_company_id = self.kwargs.get('car_company_id')
        return CarCompanyComments.objects.filter(car_company_id=car_company_id)
 

class AddCarCompany(APIView):
    serializer_class = CarCompanySerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated , IsManager]
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'object created, use the returned id to post images for it', 'id': serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddCarCompanyImage(generics.CreateAPIView):
    serializer_class = CarCompanyImageSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class AddCar(generics.CreateAPIView):
    serializer_class = CarSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated , IsManager]
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'object created, use the returned id to post images for it', 'id': serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCarImages(generics.CreateAPIView):
    serializer_class = CarImagesSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]



class AddCarReservation(APIView):
    serializer_class = CarReservationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    def post(self, request , car_id):
        car = Car.objects.get(id=car_id)
        if request.user.balance < car.price:
            return Response('not enouph balance' , status=status.HTTP_400_BAD_REQUEST)
        elif car.reserved:
            return Response('car already reserved', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'success, use the returned reservation id to add image of user credintials', 'reservation_id': serializer.data.get('id')}, status=status.HTTP_200_OK)
            else:
                return Response('not valid data', status=status.HTTP_400_BAD_REQUEST)
            


class AddCarReservationIDImage(generics.CreateAPIView):
    serializer_class = CarReservationIdImageSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  



class AddCarCompanyComment(generics.CreateAPIView):
    serializer_class = CarCompanyCommentsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  



class UpdateCarCompany(APIView):
    serializer_class = CarCompanySerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated , IsManager]
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
    permission_classes = [IsAuthenticated , IsManager]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_company_image_id):
        try:
            image = CarCompanyImages.objects.get(id=car_company_image_id)
        except CarCompanyImages.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response('success', status=status.HTTP_200_OK)


class DeleteCarImage(APIView):
    permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_image_id):
        try:
            image = CarImages.objects.get(id=car_image_id)
        except CarImages.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response('success', status=status.HTTP_200_OK)



class DeleteCarCompany(APIView):
    permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_company_id):
        try:
            carcompany = CarCompany.objects.get(id=car_company_id)
        except CarCompany.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        carcompany.delete()
        return Response('success', status=status.HTTP_200_OK)    
    



class DeleteCar(APIView):
    permission_classes = [IsAuthenticated , IsManager]
    def delete(self , request , car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        car.delete()
        return Response('success', status=status.HTTP_200_OK) 


class DeleteCarCompanyComment(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self , request , car_company_comment_id):
        try:
            carcompanycomment = CarCompanyComments.objects.get(id=car_company_comment_id)
        except CarCompanyComments.DoesNotExist:
            return Response('not valid id', status=status.HTTP_404_NOT_FOUND)
        carcompanycomment.delete()
        return Response('success', status=status.HTTP_200_OK) 