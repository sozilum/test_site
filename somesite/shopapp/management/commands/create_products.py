from typing import Any, Optional
from shopapp.models import Product
from django.core.management import BaseCommand


class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Создание продукта')

        product_names = [
            'КругВерх',
            'СтолВерх',
            'УмныйТелефон'
        ]

        for i_name in product_names:
            product, created = Product.objects.get_or_create(name = i_name)
            self.stdout.write('Создан продукт {}'.format(product.name))


        self.stdout.write(self.style.SUCCESS('Продукты созданы'))