"""Modules allows to import import functions to be used int the code"""
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import transaction
from Order.models import Order, OrderItem
from cart.cart import Cart


@login_required
def checkout(request):
    """Function uses the login decorator as a user can only checkout if he/she has logged in"""
    with transaction.atomic():
        cart = Cart(request)
        total_price = cart.get_total()
        tax_pay = int((total_price / 100) * 17)
        grand_total = total_price + tax_pay
        if request.user.is_authenticated and total_price > 0:
            order = cart.create_order(request.user)
            cart.clear()
            order.save()
            messages.success(request, "Your order has been placed. Thank you!")
            return render(
                request,
                "order_details.html",
                {
                    "order": order,
                    "total_price": total_price,
                    "tax_pay": tax_pay,
                    "gt": grand_total,
                },
            )
        else:
            return render(request, "UserLogin.html")


@login_required
def order_history(request):
    """Only an authenticated user can see past orders"""
    with transaction.atomic():
        requested_user = request.user
        orders = []
        try:
            orders = Order.objects.filter(user=requested_user)
        except Order.DoesNotExist as exception:
            print(exception)
            messages.error(request, "Sorry no order exists")
    return render(request, "orders.html", {"orders": orders})


def view_order(request):
    """See all the orders available"""
    with transaction.atomic():
        order_id = request.POST["order_id"]
        order = Order.objects.get(pk=order_id)
        order_items = OrderItem.objects.filter(order=order.pk)
        print("Ordered: ", order_items)
    return render(
        request, "order_details.html", {"order": order, "order_items": order_items}
    )


def change_status(request):
    """Changes the status of a particular order"""
    with transaction.atomic():
        order_id = request.POST["order_id"]
        status = request.POST["status"]
        try:
            order = Order.objects.get(pk=order_id)
            order.status = status
            order.save()
        except Order.DoesNotExist as exception:
            print(exception)
            messages.error(request, "Cannot change the status")
    return redirect("home")


def order_by_status(request):
    """
    The function retrieves orders from the database based on the specified status and renders them along
    with the status choices and user information in the Admin_Index.html template.
    :return: a rendered HTML template called "Admin_Index.html" with the following context variables:
    "orders", "status_choices", "user", and "status".
    """
    with transaction.atomic():
        status = request.POST["status_name"]
        orders = Order.objects.filter(status=status)
        status_choices = Order.STATUS_CHOICES
    return render(
        request,
        "Admin_Index.html",
        {
            "orders": orders,
            "status_choices": status_choices,
            "user": request.user,
            "status": status,
        },
    )
