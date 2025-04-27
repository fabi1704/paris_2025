
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product
from cart.cart import Cart
import json

class CartViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart_summary_url = reverse('cart_summary')
        self.cart_add_url = reverse('cart_add')
        self.cart_delete_url = reverse('cart_delete')
        self.cart_update_url = reverse('cart_update')

        # Create a test product
        self.product = Product.objects.create(name='Marathon', solo_price=100.00)
        

    def test_cart_summary_view(self):
        response = self.client.get(self.cart_summary_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_summary.html')
        self.assertIn('cart_products', response.context)
        self.assertIn('quantities', response.context)
        self.assertIn('totals', response.context)

    def test_cart_add_view(self):
        response = self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(data['qty: '], 1)

    def test_cart_delete_view(self):
        # Add product to cart first
        cart = Cart(self.client)
        cart.add(product=self.product, quantity=2)

        response = self.client.post(self.cart_delete_url, {
            'action': 'post',
            'product_id': self.product.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(data['product'], self.product.id)

    def test_cart_update_view(self):
        # Add product to cart first
        cart = Cart(self.client)
        cart.add(product=self.product, quantity=2)

        response = self.client.post(self.cart_update_url, {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 3)
