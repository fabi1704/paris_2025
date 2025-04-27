from .cart import Cart

# Create context processor so our cart is functional on all pages of the website
def cart(request):
    # Return the default data from our Cart
    return {'cart' : Cart(request)}