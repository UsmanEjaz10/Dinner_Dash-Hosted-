from django.contrib import messages
from django.shortcuts import render, redirect
from decimal import Decimal
from Item import views
from Item.models import Item
from cart.cart import Cart


def add_to_cart1(request):

    item_id  = request.POST['item_id']    
    item = Item.objects.get(id=item_id)
    if item.is_retired == False:
        cart = Cart(request)
        cart.add_item(item)
        messages.success(request, f'Item has been added into the cart ')
    else:
        messages.info(request, "Sorry the item is not available at this moment.")
    
    item_list = views.Item_Handler()
    response = item_list.get(request)
        
    return response


def view_cart(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    total_price = cart.get_total()
    tax_pay = int((total_price/100)*17)
    grand_total = total_price + tax_pay
    try:
        for item_id, item_data in cart_items:
            item_data['sub_total'] = Decimal(item_data['quantity']) * Decimal(item_data['price'])
            item = Item.objects.get(pk = int(item_id))
            item_data['photo'] = item.photo.url
        print(cart_items, "---")
        
    except:
        messages.error(request, "Not found")

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'tax_pay': tax_pay, 'gt': grand_total})



def clear_cart(request):
    cart = Cart(request)
    try:
        cart.clear()
        messages.success(request, "All the items have been cleared")
    except:
        messages.error(request,"Cannot clear the cart")

    return redirect('cart_view')


def removeitem(request):
    cart = Cart(request)
    item_id = int(request.POST['item_id'])

    try:
        item = Item.objects.get(pk = item_id)
        print(item)
        cart.remove_item(item)
        messages.success(request, "Item has been removed from the cart")
    except:
        messages.warning(request, "Could not found the item")

    return redirect('cart_view')


def remove_quantity(request):
    cart = Cart(request)
    item_id = int(request.POST['item_id'])

    try:
        item = Item.objects.get(pk = item_id)
        cart.remove_quantity(item)
    except Exception as e:
        print(e)

    return redirect('cart_view')

def add_quantity(request):
    cart = Cart(request)
    item_id = int(request.POST['item_id'])

    try:
        item = Item.objects.get(pk = item_id)
        cart.add_quantity(item)
    except Exception as e:
        print(e)

    return redirect('cart_view')
