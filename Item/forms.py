from django import forms
from Item.models import Category, Item

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control m-3 form-floating '}) 



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'categories', 'photo', 'is_retired', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control m-3 form-floating '}) 

 
        self.fields['is_retired'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
 