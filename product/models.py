from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator
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
    payment_intent_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)

    def __str__(self):
        return f'Order number: {self.id}, by {self.user.username} '
        
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator])

    class Meta:
        # Ensures a product cannot be added to the same cart twice.
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.quantity} X {self.product.name}'
    
    @property
    def total_price(self):
        return self.quantity * self.product.price

