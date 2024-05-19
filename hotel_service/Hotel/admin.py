from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Hotel)
admin.site.register(HotelImages)
admin.site.register(HotelReservation)
admin.site.register(HotelReservationIdImage)
admin.site.register(HotelComments)
admin.site.register(City)
admin.site.register(Features)
admin.site.register(Stay)
admin.site.register(StayImages)