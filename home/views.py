from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

from django.views import View
from home.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
import pickle
from sklearn.linear_model import LinearRegression
from .form import UserForm , ModelForm, EmailForm
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.decorators import login_required




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
        cart[item_id] = cart.get(item_id, 0) + 1
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


def topgrossing(request):

    # making a variable to store custom form's instance (UserForm)
    custom_form = UserForm()

    # storing the form instance into a key - value dictionary
    data = {'custom_car_form' : custom_form}
    return render(request, 'topgrossing.html', data)







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





def login(request):
  
    if request.method == "POST":
        print("POST request recieved")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        print("User authentication method is called")

        if user is not None:
            obj = User.objects.get(username = username)
            per = obj.get_all_permissions()
            print("Permissions allocated are: ", per, user)
            return render(request ,"home.html")
        else:
            messages.warning(request, 'Invalid username or password')
            return render(request, 'login.html')
               
    return render(request, 'login.html')





def logout_user(request):
    logout(request)
    return redirect("/login")



# Class based views #-------------------------------------------------------------------------

class car_form(View):
    
    def get(self, request):
         # making a variable to store custom form's instance (UserForm)
        custom_form = ModelForm()

        # storing the form instance into a key - value dictionary
        data = {'custom_car_form' : custom_form}
        return render(request, 'topgrossing.html', data)

    def post(self, request):
        
        id = request.POST.get('car_id')
        model = request.POST.get('model')
        version = request.POST.get('version')
        model_year = request.POST.get('model_year')
        price_per_hour = request.POST.get('price_per_hour')
        class_type = request.POST.get('class_type')

        car_model = Car(car_id = id , model = model, version = version, model_year = model_year, price_per_hour = price_per_hour, class_type = class_type )
        car_model.save()

        return redirect('topgrossing')
    

class sendmail(View):

    def post(self, request):
        subject = request.POST.get('subject')
        msg = request.POST.get('msg')
        sender = request.POST.get('sender')
        to = request.POST.get('to')

        print(sender, " sent a mail with subject = ", subject, " and the data = ", msg, " to ", to)
        send_mail(subject, msg, sender, [to])
        return redirect('sendmail')

    def get(self, request):

        mailform = EmailForm()

        data = {'form' : mailform}

        return render(request, 'email.html', data)