from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

def product_preview_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(
        pk = instance.pk,
        filename = filename
    )


class Product(models.Model):
    """
    Модель Product представляет товар,
    который можно продовать в магазине

    Заказы тут: `shopapp.order`
    """
    class Meta:
        ordering =['name']
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discout = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete= models.PROTECT, null= True)
    preview = models.ImageField(null = True, blank= True, upload_to=product_preview_directory_path)

    def __str__(self) -> str:
        return 'Product ({} {})'.format(self.pk, self.name)

def product_image_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(
        pk = instance.product.pk,
        filename = filename
    )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name= 'images')
    image = models.ImageField(upload_to=product_image_directory_path)
    description = models.CharField(max_length= 200, null= False, blank= True)


class Order(models.Model):
    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    delivery_adress = models.TextField(null=True, blank= True)
    promocode = models.CharField(max_length=20, null= False, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null= True, upload_to='orders/receipts')