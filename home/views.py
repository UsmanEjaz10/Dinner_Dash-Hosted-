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
from .cart import Cart



# Create your views here.

# Function based views here #---------------------------------------------------------------------------------------------------------------------


class index(View):
        
      
    def post(self, request):
           
            return render(request, 'home.html')

    def get(self, request):
        return render(request, "home.html")




class about(View):

    
    def get(self, request):
        items = Item.objects.all()
        categories = Category.objects.all()
        print("get method called")
        return render(request, 'about.html', {'items' : items, 'categories': categories})

   
def getItemsByCategory(request):
        id  = request.POST['category_id']
        category = Category.objects.get(pk = id)
        items = Item.objects.filter(categories = category)
        categories = Category.objects.all()
        
        return render(request, 'about.html', {'items' : items, 'categories': categories})



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


def add_to_cart1(request):

    item_id  = request.POST['item_id']    
    item = Item.objects.get(id=item_id)
    if item.is_retired == False:
        cart = Cart(request)
        cart.add_item(item)
        messages.success(request, f'Item has been added into the cart ')
    else:
        messages.info(request, "Sorry the item is not available at this moment.")
    
    item_list = about()
    response = item_list.get(request)
        
    return response


def view_cart(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    total_price = cart.get_total()
    tax_pay = int((total_price/100)*17)
    grand_total = total_price + tax_pay
    try:
        for item_id, item_data in cart_items:
            item_data['sub_total'] = Decimal(item_data['quantity']) * Decimal(item_data['price'])
            item = Item.objects.get(pk = int(item_id))
            item_data['photo'] = item.photo.url
        print(cart_items, "---")
        
    except:
        messages.error(request, "Not found")

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'tax_pay': tax_pay, 'gt': grand_total})



def clear_cart(request):
    cart = Cart(request)
    try:
        cart.clear()
        messages.success(request, "All the items have been cleared")
    except:
        messages.error(request,"Cannot clear the cart")

    return redirect('cart_view')


@login_required
def checkout(request):
    cart = Cart(request)
    total_price = cart.get_total()
    tax_pay = int((total_price/100)*17)
    grand_total = total_price + tax_pay
    
    if request.user.is_authenticated and total_price > 0:
        order = cart.create_order(request.user)
        cart.clear() 
        order.save()
        return render(request,'order_details.html', {'order':order, 'total_price': total_price, 'tax_pay': tax_pay, 'gt': grand_total})
    else:
        return render(request, 'login.html')


def removeitem(request):
    cart = Cart(request)
    item_id = int(request.POST['item_id'])

    try:
        item = Item.objects.get(pk = item_id)
        print(item)
        cart.remove_item(item)
        messages.success(request, "Item has been removed from the cart")
    except:
        messages.warning(request, "Could not found the item")

    return redirect('cart_view')



def getItem(request):
    try:
        item_id = request.POST["item_id"]
        item = Item.objects.get(pk=item_id)
        categories = item.categories.all()
        return render(request, "itemdetails.html", {'item': item, 'categories': categories})
    except:
        return redirect('about')