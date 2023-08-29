from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("addItem", views.add_to_cart1, name="addItem"),
    path("cart", views.view_cart, name="cart_view"),
    path("cart/clear", views.clear_cart, name="clear_cart"),
    path("cart/remove", views.removeitem, name="removeitem"),
        
]