from django.core.management import BaseCommand
from typing import Any, Optional

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Start demo bulk actions')

        result = Product.objects.filter(
            name__contains = 'Smartphone'
        ).update(discout=10)

        print(result)

        # info = [
        #     ('Smartphone 1', 199),
        #     ('Smartphone 2', 199),
        #     ('Smartphone 3', 199)
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]

        # result = Product.objects.bulk_create(products)

        # for obj in result:
        #     print(obj)

        self.stdout.write('Jobs done')