"""Hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    # if any url comes with '' (blank) path send it to views.index
    path("", views.index.as_view(), name='home'),
    path("about", views.about.as_view(), name='about'),
    path("contact", views.contact, name='contact'),
    path("login", views.user_login, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("addItem", views.add_to_cart1, name="addItem"),
    path("cart", views.view_cart, name="cart_view"),
    path("cart/remove", views.clear_cart, name="clear_cart"),
    path("checkout", views.checkout, name="checkout")





    ]
