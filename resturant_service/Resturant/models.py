from django.db import models
from users.models import User
# Create your models here.

class Resturant(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to="resturant_main_image" , null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True, blank=True)
    sum_of_rates = models.DecimalField(max_digits=7, decimal_places=2 , null=True , blank=True)
    number_of_rates = models.DecimalField(max_digits=7, decimal_places=2 , null=True , blank=True)
    reservation_fee = models.DecimalField(max_digits=7 , decimal_places=2 , default=0)

    @property
    def calculate_rate(self):
        if self.sum_of_rates and self.number_of_rates:
            return self.sum_of_rates / self.number_of_rates
        else:
            return "null rate"


    def __str__(self):
        return self.name
    

class ResturantImages(models.Model):
    resturant_id = models.ForeignKey(Resturant , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="resturants")


class ResturantReservation(models.Model):
    resturant_id = models.ForeignKey(Resturant , on_delete=models.CASCADE)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    number_of_people = models.SmallIntegerField()
    note = models.TextField()

    def __str__(self):
        return "resturant reservation " + str(self.pk) + "resturant " + str(self.resturant)


class ResturantReservationIdImage(models.Model):
    reservation_id = models.ForeignKey(ResturantReservation , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="resturant_reservation_id_image")

class ResturantComments(models.Model):
    resturant_id = models.ForeignKey(Resturant , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text[:50]
    

class ResturantAdmin(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    resturant = models.OneToOneField(Resturant , on_delete=models.CASCADE)