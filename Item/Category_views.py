from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from Item.models import Category, Item
from django.views import View
from django.shortcuts import redirect, render
from .forms import CategoryForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class CategoryListView(ListView):
    model = Category
    template_name = 'Category_List.html'  

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')
    template_name = 'Category_Form.html'  

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Category_Form.html'  
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')

    def get_success_url(self):
        return self.success_url