from rest_framework import serializers
from .models import Resturant

class ResturantSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = Resturant
        fields = '__all__'