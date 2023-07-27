from timeit import default_timer
from random import randint

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
# from django.urls import reverse

from .models import Product, Order
from .forms import ProductForm, Orderform


#Обработка входных данных
def some_func(request: HttpRequest):
    products = [
        ('Бибика', randint(0, 1000000)),
        ('Телефончик', randint(0, 1000000)),
        ('Креатив присутствует', randint(0, 1000000)    )
    ]
    # products = []
    context = {
        'time_running': default_timer(),
        'products': products,
    }
    return render(request, 'shopapp/shop.html', context= context)


def group_list(request: HttpRequest):
    context = {'Group': Group.objects.prefetch_related('permissions').all()

    }
    return render(request, 'shopapp/group-list.html', context=context)


def product_list(request: HttpRequest):
    context ={
        'products': Product.objects.all()
    }
    return render(request, 'shopapp/product-list.html', context = context)


def orders_list(request:HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all()
    }
    return render(request, 'shopapp/order-list.html', context= context)

def create_product(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # url = reverse("shopapp:product_list") ???
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # Product.objects.create(**form.cleaned_data)
            form.save()
            return redirect("shopapp:product_list")
    else:
        form = ProductForm()
    context = {
        'form': form
    }

    return render(request, 'shopapp/create-product.html', context= context)


def create_order(request:HttpRequest):

    if request.method == 'POST':
        form = Orderform(request.POST)
        form.save()
        return redirect('shopapp:orders_list')
    
    else:
        form = Orderform()


    context = {
        'form':form
    }

    return render(request, 'shopapp/create-order.html', context= context)