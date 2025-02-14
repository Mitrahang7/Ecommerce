from django.shortcuts import render,redirect
from .models import Order,OrderItem
from django.contrib.auth.decorators import login_required
from core.models import Product,Customer



@login_required
def checkout_view(request):
    customer = request.user.customer  # Retrieve the customer's details from the Customer model

    # Retrieve the cart from the session
    cart = request.session.get('cart', {})
    total_price = 0
    total_quantity = 0
    cart_items = []  # This will hold product details, quantity, and price for the template

    # Loop through the items in the cart and fetch product details
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue  # Skip if the product doesn't exist (shouldn't happen if cart is valid)

        quantity = item['quantity']
        price = product.sale_price if product.on_sale else product.price
        total_price += price * quantity
        total_quantity += quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
        })

    # Handle the form submission for updating shipping address
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        customer.address = shipping_address
        customer.save()
        request.session['shipping_address'] = shipping_address
        return redirect('confirm_order')  # Redirect to the next step (e.g., order review)

    return render(request, 'checkout/checkout.html', {
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    })



@login_required
def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('view_cart')

    
    customer = request.user.customer  
   
    order = Order.objects.create(customer=customer, total_price=0, total_quantity=0, shipping_address=request.session.get('shipping_address', ''))

    total_price = 0
    total_quantity = 0

   
    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']
        price = product.sale_price if product.on_sale else product.price
        total_price += price * quantity
        total_quantity += quantity

       
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

   
    order.total_price = total_price
    order.total_quantity = total_quantity
    order.save()

  
    del request.session['cart']
    request.session.modified = True

   
    return redirect('order_success')


def order_success(request):
    return render(request, 'checkout/order_success.html')


@login_required
def order_history(request):
  orders = Order.objects.filter(customer__user=request.user)
  return render(request, 'checkout/order_history.html', {'orders': orders})
