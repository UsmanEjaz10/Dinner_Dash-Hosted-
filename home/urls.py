
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    # if any url comes with '' (blank) path send it to views.index
    path("", views.index.as_view(), name='home'),
    path("about", views.about.as_view(), name='about'),
    path("login", views.user_login, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("addItem", views.add_to_cart1, name="addItem"),
    path("cart", views.view_cart, name="cart_view"),
    path("cart/clear", views.clear_cart, name="clear_cart"),
    path("cart/remove", views.removeitem, name="removeitem"),
    path("details" , views.getItem, name="itemdetails"),
    path("items_by_category", views.getItemsByCategory, name="items_by_category")
    ]
