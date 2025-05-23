from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from payment.forms import ShippingForm
from django import forms
import json
from cart.cart import Cart


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def categories(request):
    return render(request, 'categories.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You've been logged in, Welcome!"))
            return redirect('home')
        else :
            messages.success(request, ("There was an error, please try again"))
            return redirect('login') 
    
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out, thanks for your visit!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid() :
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You've been registered successfully"))
            return redirect('home')
        else:
            messages.success(request, ("Oups, there's been a problem, please try again"))
            return redirect('register')
    else:
        return render(request,'register.html', {'form':form}) 
    


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, foo):
    # Replace hyphens with spaces
    #foo = foo.replace('-',' ')
    # Grab the category from the url
    try:
        # Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html', {'products':products,'category':category})
    except:
        messages.success(request, ("Oups, that category doesn't exist"))
        return redirect('home')