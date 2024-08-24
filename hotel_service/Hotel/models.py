from django.db import models
from users.models import User

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="city_image" , null=True, blank=True)

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to="hotel_main_image" , null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True, blank=True)
    sum_of_rates = models.DecimalField(max_digits=7, decimal_places=2 , null=True , blank=True)
    number_of_rates = models.DecimalField(max_digits=7, decimal_places=2 , null=True , blank=True)


    @property
    def calculate_rate(self):
        if self.sum_of_rates and self.number_of_rates:
            return self.sum_of_rates / self.number_of_rates
        else:
            return "null rate"

    def __str__(self):
        return str(self.pk)


class Features(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.TextField()
    icone = models.ImageField(upload_to="features_icons" , null=True, blank=True)


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hotels")



class Stay(models.Model):
    ROOM_CHOICES = [
        ("Standard" , "Standard"),
        ("Deluxe" , "Deluxe"),
        ("Suite" , "Suite"),
        ("Executive" , "Executive"),
        ("Family" , "Family"),
        ("Superior" , "Superior"),
        ("Studio" , "Studio"),
        ("Villa" , "Villa"),
        ("Bungalo" , "Bungalo"),
        ("Cottage" , "Cottage")
    ]


    hotel_id = models.ForeignKey(Hotel , on_delete=models.CASCADE)
    stay_type = models.CharField(max_length=30 , choices=ROOM_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(null=True , blank=True)


    def __str__(self):
        return str(self.pk)

class StayImages(models.Model):
    stay = models.ForeignKey(Stay , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="rooms")


class HotelReservation(models.Model):
    hotel_id = models.ForeignKey(Hotel , on_delete=models.CASCADE)
    stay_id = models.ForeignKey(Stay , on_delete=models.CASCADE)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.TextField(null=True , blank=True)
    is_hotel_reservation = models.BooleanField(default=True)
    is_car_reservation = models.BooleanField(default=False)

    @property
    def number_of_days(self):
        duration = self.end_date - self.start_date
        return duration.days

    @property
    def calculate_total_price(self):
        return self.stay_id.price * self.number_of_days

    def __str__(self):
        return "hotel_id: " + str(self.hotel_id) + " stay_id: " + str(self.stay_id) + " user_id: " + str(self.user_id)


class HotelReservationIdImage(models.Model):
    reservation_id = models.ForeignKey(HotelReservation , on_delete = models.CASCADE)
    image = models.ImageField(upload_to="hotel_reservation_id_image")

class HotelComments(models.Model):
    hotel_id = models.ForeignKey(Hotel , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text[:50]



class HotelAdmin(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    hotel = models.OneToOneField(Hotel , on_delete=models.CASCADE)
