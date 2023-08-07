from django.forms.models import BaseModelForm
from typing import Any, Callable, Dict, Optional
from timeit import default_timer
from random import randint

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.views import View

from .forms import ProductForm, Orderform, GroupForm
from .models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Бибика', randint(0, 1000000)),
            ('Телефончик', randint(0, 1000000)),
            ('Креатив присутствует', randint(0, 1000000))
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
        }
        return render(request, 'shopapp/shop.html', context= context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form':GroupForm(),
            'Group': Group.objects.prefetch_related('permissions').all()

        }
        return render(request, 'shopapp/group-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailView(DetailView):
    template_name = 'shopapp/product-detail.html'
    model = Product
    fields = 'user', 'name', 'description', 'price', 'discout'


class ProductListView(ListView):
    template_name = 'shopapp/product-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived = False)


class ProductCreateView(UserPassesTestMixin,CreateView):

    def test_func(self) -> bool | None:
        user = get_object_or_404(User, pk = self.request.user.pk)
        if user.has_perm('shopapp.add_product'):
            return True
        return False

    model = Product
    fields = 'name', 'description', 'price', 'discout' 

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('shopapp:product_list')


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discout'
    
    def test_func(self) -> bool | None:
        user = get_object_or_404(User, pk = self.request.user.pk)
        if user.is_superuser or user.has_perm('shopapp.change_product') and Product.user == self.request.user:
            return True
        return False
    

    #Так можно указать кастомный суфикс страницы и туда пересылать
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse_lazy(
            'shopapp:product_detail',
            kwargs={'pk':self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


#Имя по умолчанию формируеться по названию класса Order_list
class OrderListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects
                .select_related('user')
                .prefetch_related('products'))
    #Моно указать context для изменения имени обращения 


class OrderDetailView(PermissionRequiredMixin, DetailView):
        permission_required = 'shopapp.view_order'
        queryset = (Order.objects
                .select_related('user')
                .prefetch_related('products'))


class OrderCreateView(CreateView):
    model = Order
    fields = 'user','products' , 'delivery_adress', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user','products' , 'delivery_adress', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse_lazy(
            'shopapp:order_detail',
            kwargs={'pk':self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')