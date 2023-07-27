from django.core import validators
from django import forms

from .models import Product, Order

#Так делать не надо
# class ProductForm(forms.Form):
#     name = forms.CharField(max_length= 100)
#     price = forms.DecimalField(min_value= 1, max_value= 100000, decimal_places= 2)
#     description = forms.CharField(label= 'Описание продукта', 
#                                   widget= forms.Textarea(attrs={'rows':5, 'cols': 30}), 
#                                   validators= [validators.RegexValidator(
#                                       regex= r'great',
#                                       message= 'Поле должно содержать слово "great"'
#                                   )])

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discout'

class Orderform(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'products', 'delivery_adress', 'promocode'