from django.forms.models import BaseModelForm
from timeit import default_timer
from random import randint

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views import View

from .models import Product, Order
from .forms import GroupForm


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


class ProductCreateView(PermissionRequiredMixin,CreateView):

    def has_permission(self) -> bool | None:
        if self.request.user.has_perm('shopapp.add_product'):
            return True
        return False

    model = Product
    fields = 'name', 'description', 'price', 'discout'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('shopapp:product_list')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discout'
    
    def has_permission(self) -> bool:
        if self.request.user.is_superuser or self.request.user.has_perm('shopapp.change_product') and self.get_object().user == self.request.user:
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


class ProductDaaExportView(View):
    def get(self, requests:HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price':product.price,
                'archived':product.archived
            }
            for product in products
        ]
        return JsonResponse({'products': products_data})