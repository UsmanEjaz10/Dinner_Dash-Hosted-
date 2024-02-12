"""Module allows us to use function to display error or success messages"""
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate, logout, login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from Order.models import Order
from .forms import UserForm


class Authenticate(View):
    """view takes a respective user to its respective landing page"""

    def post(self, request):
        """Handles post requests"""
        return render(request, "home.html")

    def get(self, request):
        """Identifies user type and redirects him/her to authorized page"""
        if request.user.is_superuser:
            orders = Order.objects.all()
            status_choices = Order.STATUS_CHOICES
            return render(
                request,
                "Admin_Index.html",
                {
                    "orders": orders,
                    "status_choices": status_choices,
                    "user": request.user,
                },
            )
        else:
            return render(request, "home.html", {"user": request.user})


def user_login(request):
    """login function to authenticate user"""
    if request.method == "POST":
        with transaction.atomic():
            print("POST request recieved")
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            print("User authentication method is called")

            if user is not None:
                login(request, user)
                obj = User.objects.get(username=username)
                per = obj.get_all_permissions()
                print("Permissions allocated are: ", per, user)
                return redirect("home")
            else:
                messages.warning(request, "Invalid username or password")
                return render(request, "Login.html")
    return render(request, "Login.html")


def logout_user(request):
    """Clears the cart and logs out the respective user"""
    if request.user.is_authenticated == False:
        request.session.modified = False
    logout(request)
    return redirect("/login")


class UserListView(ListView):
    """View displays all the registered users"""
    model = User
    template_name = "User_List.html"


class UserCreateView(CreateView):
    """View allows a new user to signup or a superuser to create another superuser"""
    model = User
    form_class = UserForm
    template_name = "User_Form.html"
    success_url = reverse_lazy("home")


class UserUpdateView(UpdateView):
    """view class allows us to update a specific user"""
    model = User
    form_class = UserForm
    template_name = "User_Form.html"
    success_url = reverse_lazy("home")


class UserDeleteView(DeleteView):
    """view class deletes the respective user from database"""
    model = User
    success_url = reverse_lazy("user-list")
