from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, Category
from django.contrib.auth.models import User
from store.forms import SignUpForm

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.categories_url = reverse('categories')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')

        # Create a test user
        self.user = User.objects.create_user(username='pioupiou', password='Hiram2008')

        # Create a test category and product
        self.category = Category.objects.create(name='Athletics')
        self.product = Product.objects.create(name='Marathon', solo_price=10.00, category=self.category)

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Marathon')

    def test_categories_view(self):
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {
            'username': 'pioupiou',
            'password': 'Hiram2008'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'pioupiou',
            'password': 'oups'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_logout_view(self):
        self.client.login(username='pioupiou', password='Hiram2008')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_register_view_post_success(self):
        response = self.client.post(self.register_url, {
            'username': 'Bernie',
            'password1': '20Ker19Grist37',
            'password2': '20Ker19Grist37'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username='Bernie').exists())

    def test_register_view_post_failure(self):
        response = self.client.post(self.register_url, {
            'username': 'Bernie',
            'password1': '20Ker19Grist37',
            'password2': 'oups'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)

    def test_product_view(self):
        response = self.client.get(reverse('product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
        self.assertContains(response, 'Marathon')

    def test_category_view_success(self):
        response = self.client.get(reverse('category', args=[self.category.name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertContains(response, 'Marathon')

    def test_category_view_failure(self):
        response = self.client.get(reverse('category', args=['NonExistentCategory']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
