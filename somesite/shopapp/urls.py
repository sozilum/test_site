from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.urls import path, include
from .views import (ShopIndexView, GroupListView,
                    ProductListView, OrderListView, 
                    ProductCreateView, OrderCreateView, 
                    ProductDetailView, OrderDetailView,
                    ProductUpdateView, ProductDeleteView,
                    OrderUpdateView, OrderDeleteView,
                    OrderDataExportView, ProductViewSet,
                    OrderViewSet)#ProductDaaExportView

from rest_framework.routers import DefaultRouter

app_name = 'shopapp'
#Так подключить сериализаторы
routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders',OrderViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name = 'shop'),
    path('groups/', GroupListView.as_view(), name = 'groups_list'),
    path('api/', include(routers.urls)),

    path('products/', ProductListView.as_view(), name = 'product_list'),
    path('products/create/',  ProductCreateView.as_view(), name = 'product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product_detail'),
    # path('products/export/', ProductDaaExportView.as_view(), name = 'products-export'),
    path('products/<int:pk>/update/',ProductUpdateView.as_view(), name = 'product_update'),
    path('products/<int:pk>/confirm-delete/', ProductDeleteView.as_view(), name = 'product_delete'),

    path('orders/', OrderListView.as_view(), name = 'orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name = 'create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name = 'order_detail'),
    path('orders/export/', OrderDataExportView.as_view(), name = 'orders-export'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name = 'order_update'),
    path('orders/<int:pk>/confirm-delete/', OrderDeleteView.as_view(), name = 'order_delete')
]