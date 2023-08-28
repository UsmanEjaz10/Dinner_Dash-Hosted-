from django import forms
from .models import Car, Email


class UserForm(forms.Form):
    car_id = forms.IntegerField(widget=forms.TextInput(attrs={'class' :"form-control"}))
    model = forms.CharField(max_length= 50 , widget=forms.TextInput(attrs={'class' :"form-control"}))
    version = forms.CharField(max_length= 50 , widget=forms.TextInput(attrs={'class' :"form-control"}))
    model_year= forms.IntegerField(widget=forms.TextInput(attrs={'class' :"form-control"}))
    price_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'class' :"form-control"}))
    class_type = forms.CharField(max_length= 10, widget=forms.TextInput(attrs={'class' :"form-control"})) 

class ModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_id', 'model', 'version', 'model_year', 'price_per_hour', 'class_type']
        labels = {'car_id' : "Car ID" , 'model' : 'Make model' , 'version' : 'Version' , 'price_per_hour' : 'Per Hour price' , 'class_type' : 'Type'}

class EmailForm(forms.ModelForm):
    class Meta:
        model =  Email
        fields = ['subject', 'msg', 'sender' , 'to']
        labels = {'subject' : 'Subject' , 'msg' : 'Email message' , 'sender' : 'From' , 'to' : 'To'}      