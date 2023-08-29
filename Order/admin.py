from django.contrib import admin
from Order.models import Order, OrderItem

admin.site.register(OrderItem)
admin.site.register(Order)
