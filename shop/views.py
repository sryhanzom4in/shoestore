from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Order

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def manager_panel(request):
    if request.user.role not in ['manager', 'admin']:
        return redirect('index')
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(code__icontains=query) | Q(brand__icontains=query)
        )
    orders = Order.objects.all()
    return render(request, 'manager.html', {'products': products, 'orders': orders, 'query': query})

@login_required
def admin_panel(request):
    if request.user.role != 'admin':
        return redirect('index')
    products = Product.objects.all()
    orders = Order.objects.all()
    return render(request, 'admin.html', {'products': products, 'orders': orders})
