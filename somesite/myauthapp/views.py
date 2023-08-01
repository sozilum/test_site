from django.contrib.auth.views import LogoutView
# from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render, redirect
from django.urls import reverse_lazy

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('auth:login')

def cookie_get(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default_value')
    return HttpResponse(f'Cookie value: {value!r}')

def set_cookie(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie_set')
    response.set_cookie('fizz', 'buzz', max_age= 4000)
    return response

def set_session(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'eggs'
    return HttpResponse('Session set!')

def get_session(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')