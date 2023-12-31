from typing import Any
from django import http
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView
from django.utils.translation import gettext as _, ngettext
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy, reverse
from django.views import View
from random import random

from .models import Profiel


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        welcome_message = _('Welcome Hello world!')
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        product_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = product_line.format(count = items)
        return HttpResponse(f"<h1>{welcome_message}</h1> \n<h2>{products_line}</h>",
                            )


class AboutMeView(UserPassesTestMixin, UpdateView):
    template_name = 'myauthapp/about.html'
    queryset = Profiel.objects.all()
    context_object_name = 'profile'
    fields = ['profile_image']

    def test_func(self) -> bool | None:
        if self.get_object().pk == self.request.user.profiel.pk or self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return False

    def get_success_url(self) -> str:
        return reverse('authapp:about_me',
                       kwargs={'pk':int(self.get_object().pk)},
                       )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauthapp/register.html'
    success_url = reverse_lazy('authapp:about_me')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        Profiel.objects.create(user = user)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, 
                            username = username,
                            password = password
                            )
        login(request=self.request, user=user)
        
        return HttpResponseRedirect(reverse('authapp:about_me', kwargs={
            'pk':int(self.request.user.profiel.pk)
        }))

class UsersListView(ListView):
    template_name = 'myauthapp/users_list.html'
    context_object_name = 'profile'
    queryset = Profiel.objects.all()


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('authapp:users_list')

@cache_page(60 * 2)
def cookie_get(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default_value')
    return HttpResponse(f'Cookie value: {value!r} + {random()}')


@user_passes_test(lambda user: user.is_superuser)
def set_cookie(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie_set')
    response.set_cookie('fizz', 'buzz', max_age= 4000)
    return response


@permission_required('authapp.view.profiel', raise_exception= True)
def set_session(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'eggs'
    return HttpResponse('Session set!')


@login_required
def get_session(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})