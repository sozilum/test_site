from timeit import default_timer
from random import randint

from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .models import Product, Order

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