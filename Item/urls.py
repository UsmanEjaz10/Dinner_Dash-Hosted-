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
    path('categories/<int:pk>/update/', Category_views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', Category_views.CategoryDeleteView.as_view(), name='category-delete'),

    
    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('items/create/', views.ItemCreateView.as_view(), name='item-create'),
    path('items/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),


]
