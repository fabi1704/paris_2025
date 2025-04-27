from django.test import TestCase
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress

class ShippingFormTest(TestCase):
    def test_shipping_form_valid_data(self):
        form = ShippingForm(data={
            'shipping_email': 'valerie@studi.com'
        })
        self.assertTrue(form.is_valid())

    def test_shipping_form_no_data(self):
        form = ShippingForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('shipping_email', form.errors)

class PaymentFormTest(TestCase):
    def test_payment_form_valid_data(self):
        form = PaymentForm(data={
            'billing_email': 'valerie@studi.com',
            'card_name': 'Valerie Dupont',
            'card_number': '1098457392836819',
            'card_exp_date': '04/27',
            'card_cvv_number': '123',
            'card_address1': '27 avenue Leclerc',
            'card_address2': 'Apt 4B',
            'card_city': 'Longwy',
            'card_country': 'France'
        })
        self.assertTrue(form.is_valid())

    def test_payment_form_no_data(self):
        form = PaymentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)
        self.assertIn('billing_email', form.errors)
        self.assertIn('card_name', form.errors)
        self.assertIn('card_number', form.errors)
        self.assertIn('card_exp_date', form.errors)
        self.assertIn('card_cvv_number', form.errors)
        self.assertIn('card_address1', form.errors)
        self.assertIn('card_city', form.errors)
        self.assertIn('card_country', form.errors)

    def test_payment_form_missing_required_fields(self):
        form = PaymentForm(data={
            'billing_email': 'valerie@studi.com',
            'card_name': 'Valerie Dupont',
            'card_number': '1098457392836819',
            'card_exp_date': '04/27',
            'card_cvv_number': '123',
            'card_address1': '27 avenue Leclerc',
            # 'card_address2': 'Apt 4B',  # Optional field
            'card_city': 'Longwy',
            'card_country': 'France'
        })
        self.assertTrue(form.is_valid())

    def test_payment_form_invalid_email(self):
        form = PaymentForm(data={
            'billing_email': 'inconnu@inconnu.com',
            'card_name': 'Valerie Dupont',
            'card_number': '1098457392836819',
            'card_exp_date': '04/27',
            'card_cvv_number': '123',
            'card_address1': '27 avenue Leclerc',
            'card_address2': 'Apt 4B',
            'card_city': 'Longwy',
            'card_country': 'France'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('billing_email', form.errors)
