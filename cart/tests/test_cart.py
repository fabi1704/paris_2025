from django.test import TestCase, RequestFactory
from store.models import Product
from cart.cart import Cart

class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {}
        self.cart = Cart(self.request)

        # Create a test product
        self.product = Product.objects.create(name='Marathon', solo_price=100.00, duo_price=150.50, family_price=200.75)

    def test_cart_init(self):
        self.assertIn('session_key', self.request.session)
        self.assertEqual(self.cart.cart, {})

    def test_add_product_to_cart(self):
        self.cart.add(product=self.product, quantity=2)
        self.assertIn(str(self.product.id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(self.product.id)], 2)

    def test_cart_len(self):
        self.cart.add(product=self.product, quantity=2)
        self.assertEqual(len(self.cart), 1)

    def test_get_prods(self):
        self.cart.add(product=self.product, quantity=2)
        products = self.cart.get_prods()
        self.assertIn(self.product, products)

    def test_get_quants(self):
        self.cart.add(product=self.product, quantity=2)
        quantities = self.cart.get_quants()
        self.assertEqual(quantities[str(self.product.id)], 2)

    def test_update_product_quantity(self):
        self.cart.add(product=self.product, quantity=2)
        self.cart.update(product=self.product.id, quantity=3)
        self.assertEqual(self.cart.cart[str(self.product.id)], 3)

    def test_delete_product_from_cart(self):
        self.cart.add(product=self.product, quantity=2)
        self.cart.delete(product=self.product.id)
        self.assertNotIn(str(self.product.id), self.cart.cart)

    def test_cart_total(self):
        self.cart.add(product=self.product, quantity=2)
        total = self.cart.cart_total()
        expected_total = (self.product.solo_price + self.product.duo_price + self.product.family_price) * 2
        self.assertEqual(total, expected_total)

