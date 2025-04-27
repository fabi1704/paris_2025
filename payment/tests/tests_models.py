from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Product
from payment.models import ShippingAddress, Order, OrderItem
from django.utils import timezone
import datetime

class ShippingAddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='pioupiou', password='Hiram2008')
        self.shipping_address = ShippingAddress.objects.create(user=self.user, shipping_email='valerie@studi.com')

    def test_shipping_address_str(self):
        self.assertEqual(str(self.shipping_address), f'Shipping Address - {self.shipping_address.id}')

    def test_shipping_address_verbose_name_plural(self):
        self.assertEqual(str(ShippingAddress._meta.verbose_name_plural), "Shipping Address")

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='pioupiou', password='Hiram2008')
        self.order = Order.objects.create(user=self.user, email='valerie@studi.com', amount_paid=100.00)

    def test_order_str(self):
        self.assertEqual(str(self.order), f'Order - {self.order.id}')

    def test_order_auto_now_add(self):
        self.assertIsNotNone(self.order.date_ordered)

    def test_order_shipped_date(self):
        self.order.shipped = True
        self.order.save()
        self.assertIsNotNone(self.order.date_shipped)
        self.assertAlmostEqual(self.order.date_shipped, timezone.now(), delta=datetime.timedelta(seconds=1))

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='pioupiou', password='Hiram2008')
        self.product = Product.objects.create(name='Marathon', solo_price=10.00)
        self.order = Order.objects.create(user=self.user, email='valerie@studi.com', amount_paid=100.00)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, user=self.user, quantity=2, price=20.00)

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f'Order Item - {self.order_item.id}')

    def test_order_item_default_quantity(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, user=self.user, price=20.00)
        self.assertEqual(order_item.quantity, 1)
