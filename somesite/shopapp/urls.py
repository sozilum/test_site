from django.urls import path
from .views import some_func

app_name = 'Shopapp'


urlpatterns = [
    path('', some_func, name = 'shop')
]