from ast import Pass
from pickle import TRUE
from typing import Type
from unicodedata import name
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# ### Create User Model ###
class User(AbstractUser):
    Pass

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

### Car Make Model ###
class CarMake(models.Model):
    carMakeName = models.CharField(max_length=64)
    carDescription = models.CharField(max_length=64)

    def __str__(self):
        return f"Make: {self.carMakeName} Description: {self.carDescription}"
    
    # class Meta:
    #     verbose_name = "car make"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


### Car Make Model ###
class CarModel(models.Model):
    ### choice field for category dropdown, define choices inside a model class, and to define a suitably-named constant for each value ###
    SUV = 'SUV'
    TRUCK = 'TRK'
    VAN = 'VAN'
    WAGON = 'WGN'
    SEDAN = 'SDN'
    CAR_MODEL_CHOICES = [
        (SUV, 'SUV'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
        (WAGON, 'Wagon'),
        (SEDAN, 'Sedan'),
    ]
    carType = models.CharField(
        null=False,
        max_length=5,
        choices=CAR_MODEL_CHOICES,
        default=SUV,
    )
    ### fields ###
    nameCarModel = models.CharField(max_length=64)
    yearCarModel = models.DateField(null=True)
    dealerID = models.IntegerField()
    carMakeKey = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Name: {self.nameCarModel}, Type: {self.carType}, Year: {self.yearCarModel}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
