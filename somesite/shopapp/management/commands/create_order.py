from typing import Any, Optional
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from typing import Sequence

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Создание заказа с продуктами')
        #Так тоже можно
        # with transaction.atomic():
        user = User.objects.first()
        #defer - написать то, что не нужно подгружать
        # products: Sequence[Product] = Product.objects.defer('description', 'price', 'created_at').all()
        #only - подгрузить только нужное
        products: Sequence[Product] = Product.objects.only('id').all()
        order, created = Order.objects.get_or_create(
            delivery_adress= 'ул. пушкина, дом калатушкина',
            promocode = 'СУПЕПУПЕРРАСПРОДАЖА2',
            user= user
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write('Заказ создан {}'.format(order))