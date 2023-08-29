from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from datetime import datetime
from decimal import Decimal
from django.views import View
from home.models import *
from Order.models import Order, OrderItem
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, logout, login
import pickle
from sklearn.linear_model import LinearRegression
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.decorators import login_required
from home.cart import Cart

# Create your views here.


@login_required
def checkout(request, *args):
        cart = Cart(request)
        total_price = cart.get_total()
        tax_pay = int((total_price/100)*17)
        grand_total = total_price + tax_pay
    
        if request.user.is_authenticated and total_price > 0:
            order = cart.create_order(request.user)
            order.total = grand_total
            cart.clear() 
            order.save()
            return render(request,'order_details.html', {'order':order, 'total_price': total_price, 'tax_pay': tax_pay, 'gt': grand_total})
        else:
            return render(request, 'login.html')
        
@login_required
def order_history(request, *args):
        requested_user = request.user
        orders = []
        try:
            orders = Order.objects.filter(user = requested_user)
        except:
            messages.error(request, "Sorry no order exists")

        return render (request,'orders.html', {'orders':orders})

def view_order(request, *args):
    order_id = request.POST['order_id']
    order = Order.objects.get(pk = order_id)
    return render(request, "order_details.html", {'order': order})