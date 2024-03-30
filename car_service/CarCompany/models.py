from django.db import models
from users.models import User 
# Create your models here.

class CarCompany(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
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
    car_company_id = models.ForeignKey(CarCompany , on_delete=models.CASCADE)
    car_id = models.OneToOneField(Car , on_delete=models.CASCADE)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_location = models.CharField(max_length=200 , null=True , blank=True)
    delivery_location = models.CharField(max_length=200 , null=True , blank=True)
    description = models.TextField(null=True , blank=True)

    @property
    def number_of_days(self):
        duration = self.end_date - self.start_date
        return duration.days
    @property
    def calculate_total_price(self):
        return self.car_id.price * self.number_of_days
    
    def __str__(self):
        return "car_company_id: " + str(self.car_company_id) + " car_id: " + str(self.car_id) + " user_id: " + str(self.user_id)


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