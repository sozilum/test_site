"""
В этом модуле лежат различные наборый представлений. 

Разные view магазина: по товарам, заказам и т.д.
"""

from timeit import default_timer
from csv import DictWriter
from random import randint
import logging
from typing import Any
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.utils.safestring import SafeText

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import Http404
from django.views import View

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order, ProductImage
from .forms import GroupForm, ProductForm
from .utils import save_csv_product

log = logging.getLogger(__name__)

@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product

    Полный CRUD для сущностей товара
    """
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

    @method_decorator(cache_page(60 * 3))
    def list(self, *args, **kwargs):
        print('hello products list')
        return super().list(*args, **kwargs)

    @extend_schema(
        summary='Get one product by id',
        description='Retrieve **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Emty respose, product by id is not found'),
        }
    )
    def retrieve(self,*args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, reqest: Request):
        response = HttpResponse(content_type = 'text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}-export.csv'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discout',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field:getattr(product, field)
                for field in fields
            })
        return response

    @action(detail=False,
            methods=['post'],
            parser_classes = [MultiPartParser],
            )
    def upload_csv(self, request:Request):
        products = save_csv_product(
            request.FILES['file'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many = True)
        return Response(serializer.data)


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

    # @method_decorator(cache_page(60 * 3))
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
        log.debug('Products for shop index %s', products)
        log.info('Rendering shop index')
        print('shop index conext', context)
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
        cache_key = 'order_data_export'
        orders_data = cache.get(cache_key)
        
        if orders_data is None: 
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
            elem = orders_data[0]
            name = elem['user']
            cache.set(cache_key, orders_data, 300)
        print('name:', name)
        return JsonResponse({'orders': orders_data})
    

class LatestProductFeed(Feed):
    title = 'Shop feed (latest)'
    description = 'Shop update'
    link = reverse_lazy('shopapp:product_list')

    def items(self):
        return (
            Product.objects.
            select_related('user').
            filter(archived = False).
            order_by('-created_at')[:1]
        )

    def item_title(self, item: Model) -> SafeText:
        return item.name
    
    def item_description(self, item: Model) -> str:
        return item.description[:30:]
    

class UserOrderListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user-orders.html'
    model = Order
    
    def get_queryset(self) -> QuerySet[Any]:
        try:
            self.owner_pk = self.request.resolver_match.kwargs['user_id']
            self.owner = User.objects.get(pk=self.owner_pk)
            queryset = super().get_queryset()
            return queryset.filter(user = self.owner).prefetch_related('products')

        except:
            raise Http404()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {'data':super().get_context_data(**kwargs),
                   'page_owner':self.owner}
        
        return context
    


class UserOrderExportView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, user_id:int) -> HttpResponse:
        cache_key = 'order_data_export_{}'.format(user_id)
        orders_data = cache.get(cache_key)

        if orders_data is None and self.request.user.pk == user_id: 
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
            cache.set(cache_key, orders_data, 300)
        else:
            raise Http404()

        return JsonResponse({'orders': orders_data})