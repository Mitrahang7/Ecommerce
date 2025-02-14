from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('categories/', views.all_categories, name='all_categories'),
    path('search/', views.search_results, name='search_results'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
     path('logout/', views.logout_user, name='logout'),
]

