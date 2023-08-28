from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from datetime import datetime
from decimal import Decimal
from django.views import View
from home.models import *
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, logout, login
import pickle
from sklearn.linear_model import LinearRegression
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.decorators import login_required
from .cart import Cart



# Create your views here.

# Function based views here #---------------------------------------------------------------------------------------------------------------------


class index(View):
        
    @login_required    
    def post(self, request):
           
            return render(request, 'home.html')

    def get(self, request):
        return render(request, "Login.html")




class about(View):

    
    def get(self, request):
        items = Item.objects.filter(is_retired = False)
        print("i am called")
        return render(request, 'about.html', {'items' : items})


class add_to_cart(View):

    def post(self, request):
        if 'cart' not in request.session:
            request.session['cart'] = {}
    
        item_id  = request.POST['item_id']
        cart = request.session['cart']

        print(cart.get(item_id, 0))

        cart[item_id] = cart.get(item_id, 0) + 1

        print(cart[item_id], " " , item_id)
        request.session.modified = True
    
        messages.success(request, f'Item has been added into the cart ')
        item_list = about()
        response = item_list.get(request)
        
        return response
    

class CartView(View):

    def get(self, request):
        cart = request.session.get('cart', {})
    
        cart_items = []
        total_price = 0
    
        for item_id, quantity in cart.items():
            item = Item.objects.get(id=item_id)
            total_item_price = item.price * quantity
            total_price += total_item_price
        
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'total_item_price': total_item_price
            })
    
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})









def contact(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        issue = request.POST.get('issue')
        Report_Issue = Issue(username=username, phone=phone, issue=issue, date= datetime.today())
        Report_Issue.save()
        messages.success(request, 'Your issue has been sent to Admin!')
        messages.info(request, "If you don't recieve any mail regarding your issue kindly contact at XXXX-XXXXXXX or you can visit the User Handling department from 9.00 - 5.00pm on working days")
    return render(request, 'contact.html')





def user_login(request):
  
    if request.method == "POST":
        print("POST request recieved")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        print("User authentication method is called")

        if user is not None:
            login(request, user)
            obj = User.objects.get(username = username)
            per = obj.get_all_permissions()
            print("Permissions allocated are: ", per, user)
            return render(request ,"home.html")
        else:
            messages.warning(request, 'Invalid username or password')
            return render(request, 'login.html')
               
    return render(request, 'login.html')





def logout_user(request):

    if request.user.is_authenticated:
        pass
    else:
        request.session.modified = False
    logout(request)
    return redirect("/login")



def add_to_cart2(request):
    item_id  = request.POST['item_id']
    item = get_object_or_404(Item, pk=item_id)

    user = request.user
 
    order, created = Order.objects.get_or_create(user=user, status='ordered')
    
    order_item, item_created = OrderItem.objects.get_or_create(order=order, item=item, defaults={'quantity': 1})
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    
    messages.success(request, f'Item has been added into the cart ')
    item_list = about()
    response = item_list.get(request)
        
    return response
    


def view_cart1(request):
    user = request.user
    
    order = Order.objects.get_or_create(user=user, status='ordered')
    ordered_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'ordered_items': ordered_items,
    }
    return render(request, 'cart.html', context)




def add_to_cart1(request):

    item_id  = request.POST['item_id']    
    item = Item.objects.get(id=item_id)
    cart = Cart(request)
    cart.add_item(item)

    messages.success(request, f'Item has been added into the cart ')
    item_list = about()
    response = item_list.get(request)
        
    return response


def view_cart(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    total_price = cart.get_total()
    for item_id, item_data in cart_items:
        item_data['sub_total'] = Decimal(item_data['quantity']) * Decimal(item_data['price'])
    print(cart_items, "---")

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    cart_view = about()
    response = cart_view.get(request)
        
    return response



def checkout(request):
    cart = Cart(request)
    total_price = cart.get_total()
    if request.user.is_authenticated and total_price > 0:
        order = cart.create_order(request.user)
        cart.clear()  # Clear the cart after creating the order
        # Implement payment processing here
        
        return render(request,'order_detail.html', {'order':order})
    else:
        return redirect('view_cart')
