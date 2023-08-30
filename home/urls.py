
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    # if any url comes with '' (blank) path send it to views.index
    path("", views.index.as_view(), name='home'),
    path("login", views.user_login, name="login"),
    path("logout", views.logout_user, name="logout"),
    ]
