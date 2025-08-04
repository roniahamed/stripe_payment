from django.db import models
from django.contrib.auth.models import User 

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='products')
    price = models.PositiveIntegerField()
    descriptions = models.CharField(max_length=100)