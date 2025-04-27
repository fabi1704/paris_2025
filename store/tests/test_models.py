

from django.test import TestCase
from store.models import Category, Customer, Product, Order
from decimal import Decimal
import uuid
import datetime

class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name="Athletics")
        Category.objects.create(name="Swimming")

    def test_category_str(self):
        category1 = Category.objects.get(name="Athletics")
        category2 = Category.objects.get(name="Swimming")
        self.assertEqual(str(category1), "Athletics")
        self.assertEqual(str(category2), "Swimming")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "categories")

class CustomerModelTest(TestCase):
    def setUp(self):
        Customer.objects.create(
            first_name="Valerie",
            last_name="Dupont",
            email="valerie@studi.com",
            password="Hiram2008"
        )

    def test_customer_str(self):
        customer = Customer.objects.get(first_name="Valerie")
        self.assertEqual(str(customer), "Valerie Dupont")
    
    def test_customer_str(self):
        customer = Customer.objects.get(name="Dupont")
        self.assertEqual(str(customer), "Valerie Dupont")

    def test_customer_str(self):
        customer = Customer.objects.get(email="valerie@studi.com")
        self.assertEqual(str(customer), "valerie@studi.com")
    
    def test_customer_str(self):
        customer = Customer.objects.get(password="Hiram2008")
        self.assertEqual(str(customer), "Valerie Dupont")


class ProductModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Athletics")
        Product.objects.create(
            name="Marathon",
            solo_price=Decimal('100.00'),
            duo_price=Decimal('150.50'),
            family_price=Decimal('250.75'),
            category=category,
            description="Run through Paris",
        )

    def test_product_str(self):
        product = Product.objects.get(name="Marathon")
        self.assertEqual(str(product), "Marathon")

    def test_product_prices(self):
        product = Product.objects.get(name="Marathon")
        self.assertEqual(product.solo_price, Decimal('100.00'))
        self.assertEqual(product.duo_price, Decimal('150.50'))
        self.assertEqual(product.family_price, Decimal('250.75'))

class OrderModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Athletics")
        product = Product.objects.create(
            name="Marathon",
            solo_price=Decimal('100.00'),
            duo_price=Decimal('150.50'),
            family_price=Decimal('250.75'),
            category=category,
            description="Run through Paris",
        )
        customer = Customer.objects.create(
            first_name="Valerie",
            last_name="Dupont",
            email="valerie@studi.com",
            password="Hiram2008"
        )
        Order.objects.create(
            product=product,
            customer=customer,
            quantity=2,
            date=datetime.date.today(),
            status=True
        )

    def test_order_defaults(self):
        order = Order.objects.get(product__name="Marathon")
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.status, True)
        self.assertIsInstance(order.order_key, uuid.UUID)
