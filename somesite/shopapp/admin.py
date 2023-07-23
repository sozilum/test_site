from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .admin_mixins import ExportAsCVSMixin
from .models import Product, Order


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
    actions =[
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline
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