from django.shortcuts import render, redirect
from django.views import View
from .models import Car
from .form import UserForm

class car_form(View):
    
    def get(self, request):
         # making a variable to store custom form's instance (UserForm)
        custom_form = UserForm()

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