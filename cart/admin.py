from django.contrib import admin
from .models import CartItem, OrderItem, Order

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

