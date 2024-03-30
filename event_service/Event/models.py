from django.db import models
from users.models import User 
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    place = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to="event_main_image" , null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class EventImages(models.Model):
    event = models.ForeignKey(Event , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="events")


class EventGoldTicket(models.Model):
    event_id = models.ForeignKey(Event , on_delete=models.CASCADE)
    number_oF_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return "ticket id: " + str(self.pk) + " ,event id: " + str(self.event_id)
    

class EventSilverTicket(models.Model):
    event_id = models.ForeignKey(Event , on_delete=models.CASCADE)
    number_oF_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return "ticket id: " + str(self.pk) + " ,event id: " + str(self.event_id)
    


class EventReservation(models.Model):
    event_id = models.ForeignKey(Event , on_delete=models.CASCADE)
    event_gold_ticket_id = models.OneToOneField(EventGoldTicket , on_delete=models.CASCADE , null=True , blank=True)
    event_silver_ticket_id = models.OneToOneField(EventSilverTicket , on_delete=models.CASCADE , null=True , blank=True)
    user_id = models.OneToOneField(User , on_delete=models.CASCADE)
    number_of_people = models.SmallIntegerField()
    note = models.TextField(null=True , blank=True)

    def __str__(self):
        return "reservation id: " + str(self.pk) + " ,event id: " + str(self.event_id)
    

class EventReservationIdImage(models.Model):
    reservation_id = models.ForeignKey(EventReservation , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event_reservation_id_image")

class EventComments(models.Model):
    event_id = models.ForeignKey(Event , on_delete=models.CASCADE)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text[:50]


class EventAdmin(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    event = models.OneToOneField(Event , on_delete=models.CASCADE)