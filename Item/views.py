from django.shortcuts import render
from Item.models import Category, Item
from django.views import View
from django.shortcuts import redirect, render
from .forms import ItemForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class Item_Handler(View):
    def get(self, request):
        items = Item.objects.all()
        categories = Category.objects.all()
        print("get method called")

        return render(request, 'about.html', {'items' : items, 'categories': categories})
    
    
def getItemsByCategory(request):
        id  = request.POST['category_id']
        category = Category.objects.get(pk = id)
        name = category.name
        items = Item.objects.filter(categories = category)
        categories = Category.objects.all()
        
        return render(request, 'about.html', {'items' : items, 'categories': categories, 'category': name})

def getItem(request):
    try:
        item_id = request.POST["item_id"]
        item = Item.objects.get(pk=item_id)
        categories = item.categories.all()
        return render(request, "itemdetails.html", {'item': item, 'categories': categories})
    except:
        return redirect('about')
    

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

