from django.db import models
from core.models import Product,Customer
from django.utils import timezone


class Order(models.Model):
  PENDING = 'Pending'
  SHIPPED = 'Shipped'
  DELIVERED = 'Delivered'
  CANCELLED = 'Cancelled'

  ORDER_STATUS=[
    (PENDING, 'Pending'),
    (SHIPPED, 'Shipped'),
    (DELIVERED, 'Delivered'),
    (CANCELLED, 'Cancelled'),
  ]

  customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
  total_price = models.DecimalField(max_digits=10, decimal_places=2)
  total_quantity = models.PositiveIntegerField()
  status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)
  shipping_address = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Order #{self.id} by {self.customer.user.username}"
  

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f"{self.product.name} (x{self.quantity})"

