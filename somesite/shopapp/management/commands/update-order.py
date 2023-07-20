from typing import Any, Optional
from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        order = Order.objects.first()
        if not order:
            self.stdout.write('Нет заказов')
            return 
        
        products = Product.objects.all()

        for i_product in products:
            order.products.add(i_product)

        self.stdout.write(self.style.SUCCESS('Успешно добавлены продукты {}'.format(order.products.all())))