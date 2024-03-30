from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(max_length=None , use_url=True)

    class Meta:
        model = Event
        fields = '__all__'