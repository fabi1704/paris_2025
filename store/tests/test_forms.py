# Create your tests here.

#Ces tests couvrent plusieurs aspects du formulaire :

# résence des champs : Vérifie que tous les champs attendus sont présents.
# Labels et widgets : Vérifie que les labels et les attributs des widgets sont correctement définis.
# Texte d'aide : Vérifie que le texte d'aide est correct pour les champs username, password1 et password2.
# Validation des données : Vérifie que le formulaire est valide avec des données correctes et invalide avec des données manquantes.


from django.test import TestCase
from django.contrib.auth.models import User
from store.forms import SignUpForm

class SignUpFormTest(TestCase):

    def test_form_has_fields(self):
        form = SignUpForm()
        expected_fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        self.assertListEqual(list(form.fields.keys()), expected_fields)

    def test_email_field_label(self):
        form = SignUpForm()
        self.assertEqual(form.fields['email'].label, '')

    def test_email_field_widget(self):
        form = SignUpForm()
        self.assertEqual(form.fields['email'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email Address')

    def test_first_name_field_label(self):
        form = SignUpForm()
        self.assertEqual(form.fields['first_name'].label, '')

    def test_first_name_field_widget(self):
        form = SignUpForm()
        self.assertEqual(form.fields['first_name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'], 'First Name')

    def test_last_name_field_label(self):
        form = SignUpForm()
        self.assertEqual(form.fields['last_name'].label, '')

    def test_last_name_field_widget(self):
        form = SignUpForm()
        self.assertEqual(form.fields['last_name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'], 'Last Name')

    def test_username_field_widget(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'User Name')

    def test_username_field_help_text(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].help_text, '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>')

    def test_password1_field_widget(self):
        form = SignUpForm()
        self.assertEqual(form.fields['password1'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Password')

    def test_password1_field_help_text(self):
        form = SignUpForm()
        self.assertEqual(form.fields['password1'].help_text, '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>')

    def test_password2_field_widget(self):
        form = SignUpForm()
        self.assertEqual(form.fields['password2'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Confirm Password')

    def test_password2_field_help_text(self):
        form = SignUpForm()
        self.assertEqual(form.fields['password2'].help_text, '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>')

    def test_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'pioupiou',
            'first_name': 'Valerie',
            'last_name': 'Dupont',
            'email': 'valerie@studi.com',
            'password1': 'Hiram2008',
            'password2': 'Hiram2008',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6) 
