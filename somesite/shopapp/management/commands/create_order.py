from typing import Any, Optional
from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Создание заказа')

        user = User.objects.first()

        order = Order.objects.get_or_create(
            delivery_adress= 'ул. пушкина, дом калатушкина',
            promocode = 'СУПЕПУПЕРРАСПРОДАЖА',
            user= user
        )
        self.stdout.write('Заказ создан {}'.format(order))