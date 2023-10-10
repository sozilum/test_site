from io import TextIOWrapper
from csv import DictReader

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls.resolvers import URLPattern
from django.db.models.query import QuerySet
from django.contrib import admin
from django.urls import path
from typing import Any

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCVSMixin
from .forms import CSVImportForm
from .utils import save_csv_product


class ProductInline(admin.StackedInline):
    model = ProductImage

class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description='Архивирование продуктов')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived =True)


@admin.action(description='Разорхивирование продуктов')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived =False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCVSMixin):
    change_list_template = 'shopapp/products_changelist.html'

    def import_csv(self, request:HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form':form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        
        if not form.is_valid():
            context ={
                'form':form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        save_csv_product(
            file=form.files['csv_file'].file,
            encoding=request.encoding,
        )

        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')

    def get_urls(self) -> list[URLPattern]:
        urls =  super().get_urls()
        new_urls = [
            path(
                'import_product_csv/',
                self.import_csv,
                name='import_products_csv'
            ),
        ]
        return new_urls + urls


    actions =[
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
        ProductInline
    ]
    # list_display = 'pk', 'name', 'description', 'price', 'discout'
    list_display = 'pk', 'name', 'description_short', 'price', 'discout', 'archived'
    list_display_links = 'pk', 'name'

    #Строка для задания базовой сортировки, если несколько фильтров то писать через запятую
    ordering = 'pk',

    #Строка отвечает за то, в каких полях поисковик будет искать информацию
    search_fields = 'name', 'description', 'price'

    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('price options',{
            'fields': ('price', 'discout'),
            'classes': ('collapse', 'wide',)
        }),
        ('images',
            {'fields':('preview',)}
         ),
        ('Extra options', {
            'fields':('archived',),
            'classes':('collapse',),
            'description': 'Extra options. Поле "archived" скрытие от пользователя'
        })
    ]

    #Если нужно совершать действия с полем только для админки
    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 50:
            return obj.description
        else:
            return obj.description[:50:] + '...'
# admin.site.register(Product, ProductAdmin)

#Класс нужен для того, чтобы при связи "Многие-Многие" можно было посмотреть что внутри
# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline
    ]
    list_display = 'delivery_adress', 'promocode', 'created_at', 'user_verbose'

    #Запрос который загружает сразу пачку данных указанных в select_related дабы не делать 
    #множество запросов (оптимизация)
    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')
    

    #Если у пользователя не указано имя, то попробует вернуть никнейм
    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username