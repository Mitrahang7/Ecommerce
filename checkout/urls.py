from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('confirm_order', views.place_order, name='confirm_order'),
    path('success/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
]

