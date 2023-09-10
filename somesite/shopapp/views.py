from django.forms.models import BaseModelForm
from timeit import default_timer
from random import randint

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views import View

from .models import Product, Order, ProductImage
from .forms import GroupForm, ProductForm
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields =['name', 'description']
    filterset_fields =[
        'name',
        'description',
        'price',
        'discout'
    ]
    ordering_fields =[
        'name',
        'price',
        'discout'
    ]

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends =[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields =['delivery_adress', 'promocode']
    filterset_fields =[
        'delivery_adress',
        'promocode',
        'user',
        'products'
    ]
    ordering_fields =[
        'user',
        'delivery_adress',
        'receipt'
    ]


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
            'items': 1,
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
    fields = 'name', 'description', 'price', 'discout', 'preview'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('shopapp:product_list')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    
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

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product = self.object,
                image = image
            )
        return response


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


class OrderDataExportView(View):#PermissionRequiredMixin,
    # def has_permission(self) -> bool:
    #     if self.request.user.is_staff or self.request.user.is_superuser:
    #         return True
        
    #     else:
    #         return False

    def get(self, requests:HttpRequest) -> JsonResponse:

        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'user': order.user.pk,
                'adress': order.delivery_adress,
                'promocode': order.promocode,
                'products':[product.pk for product in order.products.order_by('pk').all()]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})