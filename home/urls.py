
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    # if any url comes with '' (blank) path send it to views.index
    path("", views.index.as_view(), name='home'),
    path("login", views.user_login, name="login"),
    path("logout", views.logout_user, name="logout"),

    path('user/', views.UserListView.as_view(), name='user-list'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),

    ]
