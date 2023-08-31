
from django.contrib import admin
from django.urls import path
from Order import views


urlpatterns = [
    path("checkout", views.checkout, name="checkout"),
    path("history", views.order_history, name="history"),
    path("vieworder", views.view_order, name="vieworder"),
    path("changestatus", views.change_status, name="changestatus"),
    path("orderbystatus", views.order_by_status, name="order-by-status"),
]   