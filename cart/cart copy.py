from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key, -> create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure that the cart is available on wathever page of the website
        self.cart = cart

    


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price':str(product.solo_price)}
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True


    def __len__(self):
        return len(self.cart)


    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to looup products and database model
        products = Product.objects.filter(id__in=product_ids)
        # Return cart products
        return products
    

    def get_quants(self):
        quantities = self.cart
        return quantities
    

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing


    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # Lookup those keys in our products database model
        products = Product.objects.filter(id__in = product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key, value in quantities.items():
            # Convert key str into int to add
            key = int(key)
            for product in products:
                if id == key:
                    total = total + (product.solo_price*value)+(product.duo_price*value)+(product.family_price*value)
                    
        return total
