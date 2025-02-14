from core.models import Product


class Cart():
  def __init__(self, request):
    self.request = request
    self.session=request.session
    cart= self.session.get('cart')

    if not cart:
      cart={}
      self.session['cart']=cart

    self.cart=cart

  
  def add(self, product_id, quantity=1):

    product_id=str(product_id)
    product = Product.objects.get(id=product_id)
    price = product.sale_price if product.on_sale else product.price
    

    if product_id in self.cart:

      self.cart[product_id]['quantity'] += quantity

    else:

      self.cart[product_id]= {'quantity':quantity,'product_id': product_id, 'price': price, 'sale_price': product.sale_price}

    self.save()

  
  def remove(self, product_id):

    product_id=str(product_id)

    if product_id in self.cart:

      del self.cart[product_id]

    self.save()


  def save(self):

    self.request.session['cart'] = self.cart

    self.request.session.modified = True


  def get_total_quantity(self):

    total_quantity= sum(item['quantity'] for item in self.cart.values())

    return total_quantity
  
  def update_quantity(self, product_id, quantity):
    product_id = str(product_id)
    
    if product_id in self.cart:
        if quantity <= 0:
            self.remove(product_id)  # If quantity is 0 or less, remove the item from the cart
        else:
            self.cart[product_id]['quantity'] = quantity  # Update the quantity to the new value

    self.save()

  

  def get_total_price(self):
    total_price = 0
    for item in self.cart.values():
        product = Product.objects.get(id=item['product_id'])  # Fetch the product using the product_id
        price = item['sale_price'] if product.on_sale else item['price']
        total_price += item['quantity'] * price
    return total_price

  

  def __len__(self):
    return len(self.cart)


  
  def __iter__(self):
    cart = self.cart.copy()

    for item in cart.values():
        
        product = Product.objects.get(id=item['product_id'])  
        item['product'] = product  
        item['total_price'] = item['quantity'] * item['price'] 
        item['sale_price'] = item.get('sale_price', item['price'])
        yield item


  def clear(self):
    self.session['cart'] = {}

    self.session.modified = True
