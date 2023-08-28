from django.contrib import admin
from home.models import Car, Email
from home.models import *

# Register your models here.
admin.site.register(Issue)
admin.site.register(Car)
admin.site.register(Email)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
