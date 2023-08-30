from django import forms
from Item.models import Category, Item

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'categories', 'photo', 'is_retired', 'quantity']
