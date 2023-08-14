from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission 
from shopapp.models import Product, User, Order
from django.test import TestCase, Client
from django.urls import reverse


class OrderDetailTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client()
        cls.user = User(id = 99,username = 'dog', password = make_password('123'))
        cls.user.save()
        cls.user.user_permissions.add(Permission.objects.get(codename = 'view_order'))

        cls.product = Product(user = cls.user, name = 'some_dog_product', price = '123', discout = '18'),

        #?!?!?! 
        # cls.order = Order.objects.create(id = 99, user = cls.user, promocode = 'dogy')
        # cls.order.products.set(cls.product)
        # cls.order.save()

    @classmethod
    def tearDownClass(cls) -> None:
        # cls.order.delete()
        cls.user.delete()


    def test_order_detail(self):
        self.client.login(username = 'dog', password = '123')
        response = self.client.get(reverse('shopapp:order_detail', kwargs= {'pk': self.order.pk}), HTTP_USER_AGENT = 'MOZILA')
        print(response)
        self.assertEqual(response.status_code, 200)


# class ProductsExportViewTestCase(TestCase):
#     fixtures = ['products-fixture.json']

#     def test_get_products_view(self):
#         response = self.client.get(
#             reverse_lazy('shopapp:products-export'),
#                 HTTP_USER_AGENT = 'MOZILA'
#         )
#         self.assertEqual(response.status_code, 200)
#         products = Product.objects.order_by('pk').all()
#         expected_data = [
#             {
#                 'pk': product.pk,
#                 'name': product.name,
#                 'price':product.price,
#                 'archived':product.archived
#             }
#             for product in products
#         ]
#         products_data = response.json()
#         self.assertEqual(
#             products_data['products'],
#             expected_data
#         )
