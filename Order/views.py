from django.contrib import messages
from django.shortcuts import render
from Item.models import Item
from Order.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.shortcuts import redirect
# Create your views here.


@login_required
def checkout(request, *args):
        cart = Cart(request)
        total_price = cart.get_total()
        tax_pay = int((total_price/100)*17)
        grand_total = total_price + tax_pay
    
        if request.user.is_authenticated and total_price > 0:
            try:
                order = cart.create_order(request.user)
                order.total = grand_total
                cart.clear() 
                order.save()
                return render(request,'order_details.html', {'order':order, 'total_price': total_price, 'tax_pay': tax_pay, 'gt': grand_total})
            except Exception as e:
                print(e)
                messages.error(request, "Cannot create an order")
                return redirect('about')
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
    order_items = OrderItem.objects.filter(order = order.pk)
    print("Ordered: ", order_items)
    return render(request, "order_details.html", {'order': order, 'order_items': order_items})


def change_status(request):
     order_id = request.POST['order_id']
     status = request.POST['status']
     order = Order.objects.get(pk = order_id)
     order.status = status
     order.save()
     return redirect('home')


def order_by_status(request):
     status = request.POST['status_name']
     orders = Order.objects.filter(status = status)
     status_choices  = Order.STATUS_CHOICES
     return render(request, "Admin_Index.html", {'orders': orders, 'status_choices': status_choices, 'user': request.user, 'status':status})
