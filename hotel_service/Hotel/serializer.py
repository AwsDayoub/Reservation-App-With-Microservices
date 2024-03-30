from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = Hotel
        fields = '__all__'