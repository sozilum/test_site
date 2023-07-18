from timeit import default_timer
from random import randint

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

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