from django.shortcuts import render,redirect
from .cart import Cart
from django.contrib import messages
from core.models import Product


def view_cart(request):
  cart=Cart(request)
  return render(request, 'cart/cart.html', {'cart':cart})


def add_to_cart(request, product_id):
  cart= Cart(request)
  product = Product.objects.get(id=product_id)
  cart.add(product_id=product.id, quantity=1)
  messages.success(request, f'{product.name} has been added to your cart!')
  return redirect('home')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, 'Product has been removed from your cart.')
    return redirect('view_cart')  

def update_cart(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1)) 
            if quantity > 0:
                cart = Cart(request)
                cart.update_quantity(product_id=product_id, quantity=quantity)  # Update the quantity instead of adding
                messages.success(request, 'Cart has been updated!')
            else:
                messages.error(request, 'Quantity must be greater than 0.')
        except ValueError:
            messages.error(request, 'Invalid quantity entered.')
        return redirect('view_cart')  
    return redirect('view_cart')  


