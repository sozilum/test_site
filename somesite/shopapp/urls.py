from django.urls import path
from .views import some_func, group_list, product_list, orders_list, create_product, create_order

app_name = 'shopapp'


urlpatterns = [
    path('', some_func, name = 'shop'),
    path('groups/', group_list, name = 'groups_list'),

    path('products/', product_list, name = 'product_list'),
    path('products/create/', create_product, name = 'create_product'),
    
    path('orders/', orders_list, name = 'orders_list'),
    path('orders/create/', create_order, name = 'create_order'),
]