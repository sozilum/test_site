from django.urls import path
from .views import (ShopIndexView, GroupListView,
                    ProductListView, OrderListView, 
                    ProductCreateView, OrderCreateView, 
                    ProductDetailView, OrderDetailView,
                    ProductUpdateView, ProductDeleteView,
                    OrderUpdateView, OrderDeleteView)

app_name = 'shopapp'


urlpatterns = [
    path('', ShopIndexView.as_view(), name = 'shop'),
    path('groups/', GroupListView.as_view(), name = 'groups_list'),

    path('products/', ProductListView.as_view(), name = 'product_list'),
    path('products/create/', ProductCreateView.as_view(), name = 'product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product_detail'),
    path('products/<int:pk>/update/',ProductUpdateView.as_view(), name = 'product_update'),
    path('products/<int:pk>/confirm-delete/', ProductDeleteView.as_view(), name = 'product_delete'),

    path('orders/', OrderListView.as_view(), name = 'orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name = 'create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name = 'order_detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name = 'order_update'),
    path('orders/<int:pk>/confirm-delete/', OrderDeleteView.as_view(), name = 'order_delete')
]