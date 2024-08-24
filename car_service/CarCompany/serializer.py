from rest_framework import serializers
from .models import CarCompany , CarCompanyImages , Car , CarImages , CarReservation , CarReservationIdImage , CarCompanyComments, City


class CitySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = City
        fields = '__all__'



class CarCompanySerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = CarCompany
        fields = ['id', 'name' , 'email' , 'phone' , 'country' , 'city' , 'main_image' , 'date_created' , 'sum_of_rates' , 'number_of_rates']

class CarCompanyImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True)
    class Meta:
        model = CarCompanyImages
        fields = ['id' , 'car_company', 'image']


class CarCompanyWithImagesSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(max_length=None , use_url=True)
    images = CarCompanyImageSerializer(many=True , read_only=True)
    class Meta:
        model = CarCompany
        fields = ['id' , 'name' , 'email' , 'phone' , 'country' , 'city' , 'main_image' , 'date_created' , 'sum_of_rates' , 'number_of_rates' , 'images']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id' , 'car_company_id' , 'name' , 'number' , 'car_type' , 'number_of_people_can_contain' , 'contain_baby_seat' , 'price' , 'description' , 'reserved']


class CarImagesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True)
    class Meta:
        model = CarImages
        fields = ['id' , 'car' , 'image']


class CarWithCarImagesSerializer(serializers.ModelSerializer):
    images = CarImagesSerializer(many=True , read_only=True)
    class Meta:
        model = Car
        fields = ['id' , 'car_company_id' , 'name' , 'number' , 'car_type' , 'number_of_people_can_contain' , 'contain_baby_seat' , 'price' , 'description' , 'reserved' , 'images']


class CarReservationSerializer(serializers.ModelSerializer):
    car_company_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    car_type = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    carcompany_image = serializers.SerializerMethodField()
    carcompany_name = serializers.SerializerMethodField()
    carcompany_sumofrates = serializers.SerializerMethodField()
    carcompany_numberofrates = serializers.SerializerMethodField()
    carcompany_email = serializers.SerializerMethodField()
    carcompany_datecreated = serializers.SerializerMethodField()
    carcompany_country = serializers.SerializerMethodField()
    carcompany_phone = serializers.SerializerMethodField()
    class Meta:
        model = CarReservation
        fields = ['id', 'car_company', 'car', 'user', 'start_date', 'end_date', 'pickup_location', 'delivery_location', 'description', 'car_company_name', 'first_name', 'last_name', 'username', 'email', 'car_type', 'price', 'calculate_total_price', 'carcompany_image', 'carcompany_name', 'carcompany_sumofrates', 'carcompany_numberofrates', 'carcompany_email', 'carcompany_datecreated', 'carcompany_country', 'carcompany_phone', 'carcompany_email', 'is_car_reservation', 'is_hotel_reservation']

    def get_car_company_name(self, obj):
        return obj.car_company.name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_car_type(self, obj):
        return obj.car.car_type

    def get_price(self, obj):
        return obj.car.price

    def get_carcompany_image(self, obj):
        if obj.car_company.main_image:
            return obj.car_company.main_image.url  # Returns the URL of the image if it exists
        else:
            return None  # Or return a default image URL or path

    def get_carcompany_name(self, obj):
        return obj.car_company.name

    def get_carcompany_sumofrates(self, obj):
        return obj.car_company.sum_of_rates

    def get_carcompany_numberofrates(self, obj):
        return obj.car_company.number_of_rates

    def get_carcompany_datecreated(self, obj):
        return obj.car_company.date_created

    def get_carcompany_country(self, obj):
        return obj.car_company.country

    def get_carcompany_phone(self, obj):
        return obj.car_company.phone

    def get_carcompany_email(self, obj):
        return obj.car_company.email




class CarReservationPostSerializer(serializers.Serializer):
    car_company_id = serializers.IntegerField()
    car_id = serializers.IntegerField()
    username = serializers.CharField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    pickup_location = serializers.CharField(required=False, allow_blank=True)
    delivery_location = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ['car_company_id', 'car_id', 'username', 'start_date', 'end_date', 'pickup_location', 'delivery_location', 'description']

# class CarReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarReservation
#         fields = '__all__'




class CarReservationIdImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True)
    class Meta:
        model = CarReservationIdImage
        fields = ['reservation_id' , 'image']

class CarReservationWithIdImageSerializer(serializers.ModelSerializer):
    images = CarReservationIdImageSerializer(many=True , read_only=True)
    class Meta:
        model = CarReservation
        fields = ['id' , 'car_company' , 'car' , 'user' , 'start_date' , 'end_date' , 'pickup_location' , 'delivery_location' , 'description' , 'images']


class CarCompanyCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCompanyComments
        fields = '__all__'

class BalanceSerializer(serializers.Serializer):
    username = serializers.CharField()
    balance = serializers.IntegerField()
    class Meta:
        fields = ['username', 'balance']
