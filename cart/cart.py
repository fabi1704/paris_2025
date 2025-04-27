from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key, -> create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure that the cart is available on whatever page of the website
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        # Logic
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += product_qty
        else:
            self.cart[product_id] = {
                'price': str(product.solo_price),
                'quantity': product_qty
            }

        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in the database model
        products = Product.objects.filter(id__in=product_ids)
        # Return cart products
        return products

    def get_quants(self):
        return {product_id: item['quantity'] for product_id, item in self.cart.items()}

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_qty

        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def cart_total(self):
        # Get product IDs
        product_ids = self.cart.keys()
        # Lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for product_id, item in quantities.items():
            product = products.get(id=product_id)
            total += (product.solo_price * item['quantity']) + (product.duo_price * item['quantity']) + (product.family_price * item['quantity'])

        return total
