from typing import Any
from django import http
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views import View


from .models import Profiel


class AboutMeView(UpdateView):
    template_name = 'myauthapp/about.html'
    queryset = Profiel.objects.all()
    context_object_name = 'profile'
    fields = 'profile_image',
    
    def get_success_url(self) -> str:
        return reverse('authapp:about_me',
                       kwargs={'pk':int(self.object.pk)},
                       )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauthapp/register.html'
    success_url = reverse_lazy('authapp:about_me')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        Profiel.objects.create(user = self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, 
                            username = username,
                            password = password
                            )
        login(request=self.request, user=user)
        
        return response


class UsersListView(ListView):
    template_name = 'myauthapp/users_list.html'
    context_object_name = 'profile'
    queryset = Profiel.objects.all()


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('authapp:users_list')


def cookie_get(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default_value')
    return HttpResponse(f'Cookie value: {value!r}')


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