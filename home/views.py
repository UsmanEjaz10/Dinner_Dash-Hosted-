from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from Order.models import Order
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import UserForm
from django.core.paginator import Paginator


# Create your views here.

# Function based views here #---------------------------------------------------------------------------------------------------------------------


class index(View):
        
      
    def post(self, request):
           
        return render(request, 'home.html')

    def get(self, request):

        if request.user.is_superuser:
            orders = Order.objects.all()
            status_choices  = Order.STATUS_CHOICES
            return render(request, "Admin_Index.html", {'orders': orders, 'status_choices': status_choices, 'user': request.user})
        else:
            return render(request, "home.html", {'user': request.user})





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
            return redirect('home')
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


class UserListView(ListView):
    model = User
    template_name = 'User_List.html' 

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'User_Form.html' 
    success_url = reverse_lazy('home')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'User_Form.html' 
    success_url = reverse_lazy('home')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user-list')

