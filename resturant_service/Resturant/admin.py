from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Resturant)
admin.site.register(ResturantImages)
admin.site.register(ResturantReservation)
admin.site.register(ResturantReservationIdImage)
admin.site.register(ResturantComments)