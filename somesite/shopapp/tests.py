from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission 
from shopapp.models import Product, User, Order
from django.test import TestCase, Client
from django.urls import reverse
import re


class OrderDetailTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create(username = 'dog', password = make_password('123'))
        cls.user.user_permissions.add(Permission.objects.get(codename = 'view_order'))

        cls.product = Product.objects.create(user = cls.user, name = 'some_dog_product', price = '123', discout = '18'),

        cls.order = Order.objects.create(user = cls.user, promocode = 'dogy', delivery_adress = 'some_adress 123')
        cls.order.products.set(cls.product)


    @classmethod
    def tearDownClass(cls) -> None:
        cls.order.delete()


    def test_order_detail(self):
        self.client.login(username = 'dog', password = '123')
        response = self.client.get(reverse('shopapp:order_detail', kwargs= {'pk': self.order.pk}), HTTP_USER_AGENT = 'MOZILA')
        self.assertEqual(response.status_code, 200)
        
        content = str(response.content)
        delivery_adress = re.findall('Delivery address: ([a-z,A-Z,1-9, ,_]+)', content)
        promocode = re.findall('Promocode: <code>([a-z,A-Z,1-9, ,_]+)</code>', content)

        if delivery_adress[0] == self.order.delivery_adress and promocode[0] == self.order.promocode:
            print('delivery_adress and promocode are matching with order')
        
        else:
            raise ValueError


class OrderExportTestCase(TestCase):
    fixtures = ['order_data.json',
                'product_data.json',
                'user_data.json']

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create(username = 'dog2', password = make_password('123'))


    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()


    def setUp(self) -> None:
        self.user.is_staff
        self.client.login(username = 'dog2', password = '123')


    def test_order_export(self):
        
        response = self.client.get(path=reverse('shopapp:orders-export'),
            HTTP_USER_AGENT = 'MOZILA'
            )
        
        self.assertEqual(response.status_code, 200)

        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'user': order.user.pk,
                'adress': order.delivery_adress,
                'promocode': order.promocode,
                'products':[product.pk for product in order.products.order_by('pk').all()]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)