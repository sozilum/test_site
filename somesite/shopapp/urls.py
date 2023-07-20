from django.urls import path
from .views import some_func, group_list, product_list, orders_list

app_name = 'Shopapp'


urlpatterns = [
    path('', some_func, name = 'shop'),
    path('groups/', group_list, name = 'groups_list'),
    path('products/', product_list, name = 'product_list'),
    path('orders/', orders_list, name = 'orders_list')
]