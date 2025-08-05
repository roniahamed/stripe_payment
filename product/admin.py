from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','payment_intent_id', 'created_at', 'is_paid', 'is_refunded']

admin.site.register(Order, OrderAdmin)
