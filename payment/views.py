from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product

#from store.models import Customer

# Create your views here.


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    # checkout as logged in user
    if request.user.is_authenticated:
        return render(request, "payment/checkout.html", {"cart_products": cart_products, 
                                                 "quantities":quantities, "totals":totals})
    else:
        # A CHANGER
        return render(request, "payment/checkout.html", {"cart_products": cart_products, 
                                                 "quantities":quantities, "totals":totals})



def payment_success(request):

    return render(request, "payment/payment_success.html", {})


def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session to recover email info
        my_billing = request.POST
        request.session['my_billing'] = my_billing

        #Check if user is logged in
        if request.user.is_authenticated:
            # Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, 
                                                 "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            # user not logged in
             # Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, 
                                                 "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})


        #shipping_form = request.POST
        #return render(request, "payment/billing_info.html", {"cart_products": cart_products, 
                                                 #"quantities":quantities, "totals":totals, "shipping_form":shipping_form})

    else:
        messages.success(request, "Access Denied")
        return redirect('home')



def process_order(request):
    if request.POST:
        # Let's get the billing info from previous page
        payment_form = PaymentForm(request.POST or None)
        # Get billing info
        my_billing = request.session['my_billing']
        # Get billing_email 
        # billing_email = my_billing.billing_email
        
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # let's gather order information
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            amount_paid = totals
            # Create an order
            create_order = Order(user=user, amount_paid = amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get product info
            for product in cart_products():
                product_id = product.id
                price = product.solo_price
                #product_price_duo = product.duo_price
                #product_price_family = product.family_price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order_item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id , user=user ,quantity=value , price=price )
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]



            messages.success(request, "Check your emails, your order has been sent, Thank You !")
            return redirect('home')
        else :
            # Not logged in
            create_order = Order(amount_paid = amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get product info
            for product in cart_products():
                product_id = product.id
                price = product.solo_price
                #product_price_duo = product.duo_price
                #product_price_family = product.family_price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order_item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id,quantity=value , price=price )
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]



            messages.success(request, "Please log in to place your order")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')