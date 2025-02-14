from django.shortcuts import render,redirect
from .models import Product,Category
from django.db.models  import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def home(request):
  products= Product.objects.all()
  categories = Category.objects.all()[:3]
  return render(request, 'home.html', {'products':products, 'categories': categories})


def product_detail(request, id):
  product= Product.objects.get(id=id)

  return render(request, 'product_detail.html', {'product':product})

def category_products(request, category_id):
  category = Category.objects.get(id=category_id)
  products = Product.objects.filter(category=category)

  return render(request, 'category_products.html', {'products':products, 'category': category})

def all_categories(request):
  categories = Category.objects.all()
  return render(request, 'all_categories.html', {'categories': categories})

def search_results(request):
  query=  request.GET.get('q', '')

  if query:
    results = Product.objects.filter(
       Q(name__icontains=query) |Q(category__name__icontains=query) | Q(description__icontains=query) |
        Q(name__icontains=query)
    )
  
  else:
    results = Product.objects.none()  

  return render(request, 'search_results.html', {'results': results, 'query': query})


def register_user(request):
  if request.method == 'POST':
    username= request.POST.get('username')
    first_name= request.POST.get('first_name')
    last_name= request.POST.get('last_name')
    email= request.POST.get('email')
    password1= request.POST.get('password1')
    password2= request.POST.get('password2')

    if password1 != password2:
      messages.error(request, 'Password didnt match')
      return redirect('register')
    
    if  User.objects.filter(username=username).exists():
      messages.error(request, 'Username already taken')
      return redirect('register')
    
    if  User.objects.filter(email=email).exists():
      messages.error(request, 'Email already taken')
      return redirect('register')
    
    user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email, password=password1)

    user.save()
  
    login(request,user)
    messages.success(request, 'Account created successfully')
    return redirect('home')
  
  else:
    return render(request, 'register.html')
    






def login_user(request):
  if request.method == "POST":
    username= request.POST['username']
    password= request.POST['password']

    user= authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, 'You are successfully logged in')
      return redirect ('home')
    
    else:
      messages.error(request, 'Password didnot match')
      return redirect ('login')

  return render(request, 'login.html')



def logout_user(request):
  logout(request)
  messages.success( request,'You are successfully logged out')
  return redirect('home')


