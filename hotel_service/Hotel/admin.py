from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Hotel)
admin.site.register(HotelImages)
admin.site.register(HotelReservation)
admin.site.register(HotelReservationIdImage)
admin.site.register(HotelComments)
admin.site.register(Room)
admin.site.register(RoomImages)