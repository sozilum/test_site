from django.core.management import BaseCommand
from typing import Any, Optional
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Start demo bulk actions')

        # result = Product.objects.filter(name__contains='Smartphone').aggregate(
        #     Avg('price'),
        #     Max('price'),
        #     min_price = Min('price'),
        #     count = Count('id')
        # )
        # print(result)

        orders = Order.objects.annotate(
            total = Sum('products__price', default = 0),
            products_count = Count('products')
        )

        for order in orders:
            print(f'Order #{order.id} '
                  f'with {order.products_count}'
                  f'product worth {order.total}')

        self.stdout.write('Jobs done')