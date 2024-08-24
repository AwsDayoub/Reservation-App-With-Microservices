from rest_framework import serializers
from .models import Hotel , City, Features, HotelImages, Stay, StayImages, HotelComments, HotelReservation




class HotelSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = Hotel
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = City
        fields = '__all__'

class HotelFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'

class HotelImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImages
        fields = '__all__'


class StayImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayImages
        fields = '__all__'


class StaySerializer(serializers.ModelSerializer):
    stay_images = StayImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Stay
        fields = ['id', 'hotel_id', 'stay_type', 'price', 'description', 'stay_images']



class HotelCommentsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = HotelComments
        fields = '__all__'

    def get_username(self, obj):
        return obj.user.username


class HotelBigSerializer(serializers.ModelSerializer):
    hotel_images = HotelImagesSerializer(many=True, read_only=True)
    features = HotelFeaturesSerializer(many=True, read_only=True)
    stays = StaySerializer(many=True, read_only=True)
    comments = HotelCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['name', 'email', 'phone', 'country', 'city', 'main_image', 'date_created', 'sum_of_rates', 'number_of_rates', 'hotel_images', 'features', 'stays', 'stays_images', 'comments']



class ReservationSerializer(serializers.ModelSerializer):
    hotel_name = serializers.SerializerMethodField()
    hotel_image = serializers.SerializerMethodField()
    hotel_email = serializers.SerializerMethodField()
    hotel_phone = serializers.SerializerMethodField()
    hotel_country = serializers.SerializerMethodField()
    hotel_datecreated = serializers.SerializerMethodField()
    hotel_sumofrates = serializers.SerializerMethodField()
    hotel_numberofrates = serializers.SerializerMethodField()
    user_firstname = serializers.SerializerMethodField()
    user_lastname = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    stay_staytype = serializers.SerializerMethodField()
    stay_price = serializers.SerializerMethodField()

    class Meta:
        model = HotelReservation
        fields = ['hotel_id', 'stay_id', 'user_id', 'start_date', 'end_date', 'note', 'hotel_name', 'hotel_image', 'hotel_email', 'hotel_phone', 'hotel_country', 'hotel_datecreated', 'hotel_sumofrates', 'hotel_numberofrates', 'user_firstname', 'user_lastname', 'user_username', 'user_email', 'stay_staytype', 'stay_price', 'calculate_total_price', 'is_hotel_reservation', 'is_car_reservation']

    def get_hotel_name(self, obj):
        return obj.hotel_id.name

    def get_hotel_image(self, obj):
        if obj.hotel_id.main_image:
            return obj.hotel_id.main_image.url  # Returns the URL of the image if it exists
        else:
            return None  # Or return a default image URL or path


    def get_hotel_email(self, obj):
        return obj.hotel_id.email

    def get_hotel_phone(self, obj):
        return obj.hotel_id.phone

    def get_hotel_country(self, obj):
        return obj.hotel_id.country

    def get_hotel_datecreated(self, obj):
        return obj.hotel_id.date_created

    def get_hotel_sumofrates(self, obj):
        return obj.hotel_id.sum_of_rates

    def get_hotel_numberofrates(self, obj):
        return obj.hotel_id.number_of_rates

    def get_user_firstname(self, obj):
        return obj.user_id.first_name

    def get_user_lastname(self, obj):
        return obj.user_id.last_name

    def get_user_username(self, obj):
        return obj.user_id.username

    def get_user_email(self, obj):
        return obj.user_id.email

    def get_stay_staytype(self, obj):
        return obj.stay_id.stay_type

    def get_stay_price(self, obj):
        return obj.stay_id.price



class ReservationPostSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField()
    stay_id = serializers.IntegerField()
    username = serializers.CharField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    note = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ['hotel_id', 'stay_id', 'username', 'start_date', 'end_date', 'note']


class BalanceSerializer(serializers.Serializer):
    username = serializers.CharField()
    balance = serializers.IntegerField()
    class Meta:
        fields = ['username', 'balance']
