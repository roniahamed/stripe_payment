from django.db import models
from django.contrib.auth.models import User 

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='products')
    price = models.PositiveIntegerField()
    descriptions = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order number: {self.id}, by {self.user.username} '
        