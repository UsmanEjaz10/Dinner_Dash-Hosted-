from django.urls import path
from cart import views

urlpatterns = [
    path("addItem", views.add_to_cart1, name="addItem"),
    path("cart", views.view_cart, name="cart_view"),
    path("cart/clear", views.clear_cart, name="clear_cart"),
    path("cart/remove", views.removeitem, name="removeitem"),
    path("cart/remove-quantity", views.remove_quantity, name="remove-quantity"),
    path("cart/add-quantity", views.add_quantity, name="add-quantity"),    

]