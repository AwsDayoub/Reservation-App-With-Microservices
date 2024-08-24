from django.db import models
from users.models import User
from django.utils import timezone
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="city_image" , null=True, blank=True)

class CarCompany(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    #city = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to="car_company_main_image" , null=True, blank=True)
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
        return self.name


class CarCompanyImages(models.Model):
    car_company = models.ForeignKey(CarCompany , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="car_companies")


class Car(models.Model):
    CAR_CHOICES = [
        ("Economy" , "Economy"),
        ("Compact" , "Compact"),
        ("Mid_Size" , "Mid_Size"),
        ("Full_Size" , "Full_Size"),
        ("Luxury" , "Luxury"),
        ("SUV" , "SUV"),
        ("Minivan" , "Minivan"),
        ("Convertible" , "Convertible"),
        ("Sport" , "Sport"),
        ("Electric" , "Electric")
    ]
    car_company_id = models.ForeignKey(CarCompany , on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50 , choices=CAR_CHOICES)
    number_of_people_can_contain = models.SmallIntegerField()
    contain_baby_seat = models.BooleanField()
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    description = models.TextField(null=True , blank=True)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

class CarImages(models.Model):
    car = models.ForeignKey(Car , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="cars")


class CarReservation(models.Model):
    car_company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=5))
    pickup_location = models.CharField(max_length=200, null=True, blank=True)
    delivery_location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_car_reservation = models.BooleanField(default=True)
    is_hotel_reservation = models.BooleanField(default=False)
    @property
    def number_of_days(self):
        duration = self.end_date - self.start_date
        return duration.days

    @property
    def calculate_total_price(self):
        return self.car.price * self.number_of_days

    def __str__(self):
        return f"reservation_id: {self.pk}, car_company_id: {self.car_company.id}, car_id: {self.car.id}, user_id: {self.user.id}"


class CarReservationIdImage(models.Model):
    reservation_id = models.ForeignKey(CarReservation , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="car_reservation_id_image")

class CarCompanyComments(models.Model):
    car_company_id = models.ForeignKey(CarCompany , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class CarCompanyAdmin(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    carcompany = models.OneToOneField(CarCompany , on_delete=models.CASCADE)
