from django.contrib.auth.models import Group
from django import forms

from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discout'

class Orderform(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'products', 'delivery_adress', 'promocode'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',