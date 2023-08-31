from django.shortcuts import render
from Item.models import Category, Item
from django.views import View
from django.shortcuts import redirect, render
from .forms import ItemForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction

# The Item_Handler class is a view that handles item-related operations.
class Item_Handler(View):
    def get(self, request):
        with transaction.atomic():
            items = Item.objects.all()
            categories = Category.objects.all()
        print("get method called")

        return render(request, 'about.html', {'items' : items, 'categories': categories})
    
    
def getItemsByCategory(request):
    """
    The function `getItemsByCategory` retrieves all items belonging to a specific category and renders
    them along with the category name and all categories to the 'about.html' template.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, and any data
    sent with the request
    :return: a rendered HTML template called 'about.html' with the following context variables: 'items',
    'categories', and 'category'.
    """
    with transaction.atomic():
            id  = request.POST['category_id']
            category = Category.objects.get(pk = id)
            name = category.name
            items = Item.objects.filter(categories = category)
            categories = Category.objects.all()
        
    return render(request, 'about.html', {'items' : items, 'categories': categories, 'category': name})

def getItem(request):
    """
    The getItem function retrieves a specific item based on the item_id provided in the request and
    displays its details on an info page.
    """
    with transaction.atomic():
        try:
            item_id = request.POST["item_id"]
            item = Item.objects.get(pk=item_id)
            categories = item.categories.all()
            return render(request, "itemdetails.html", {'item': item, 'categories': categories})
        except:
            return redirect('about')
    

# Item Registration CRUD operation classes
class ItemListView(ListView):
    model = Item
    template_name = 'Item_List.html' 

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'Item_Form.html' 
    success_url = reverse_lazy('item-list')


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'Item_Form.html' 
    success_url = reverse_lazy('item-list')


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('item-list')

