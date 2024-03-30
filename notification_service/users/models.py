from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    TYPE = [
        ('Customer' , 'Customer') , 
        ('HotelAdmin' , 'HotelAdmin') , 
        ('CarCompanyAdmin' , 'CarCompanyAdmin'),
        ('EventAdmin' , 'EventAdmin'),
        ('ResturantAdmin' , 'ResturantAdmin')]
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    balance = models.IntegerField(null=True, blank=True, default=0)
    email_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to="user_profile_image" , null=True , blank=True)
    user_type = models.CharField(max_length=50, choices=TYPE , default='Customer')

    def __str__(self):
        return str(self.pk)



