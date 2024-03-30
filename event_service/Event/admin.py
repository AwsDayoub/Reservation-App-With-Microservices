from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Event)
admin.site.register(EventImages)
admin.site.register(EventReservation)
admin.site.register(EventReservationIdImage)
admin.site.register(EventGoldTicket)
admin.site.register(EventSilverTicket)
admin.site.register(EventComments)