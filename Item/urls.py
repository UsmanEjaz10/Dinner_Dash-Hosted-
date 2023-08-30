from django.contrib import admin
from django.urls import path
from Item import views
from Item import Category_views



urlpatterns = [
    path("details" , views.getItem, name="itemdetails"),
    path("items_by_category", views.getItemsByCategory, name="items_by_category"),
    path("about", views.Item_Handler.as_view(), name='about'), 

    path('categories/', Category_views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', Category_views.CategoryCreateView.as_view(), name='category-create'),
    
]
