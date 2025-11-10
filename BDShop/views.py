from django.shortcuts import render
from store.models import Product 
from django.shortcuts import render, get_object_or_404


def home(request):
    products = Product.objects.filter(available=True) 
    context = {
        'products': products
    }
    return render(request, 'home.html', context) 


def contact(request):
    context = {
        'address': 'Sylhet, Bangladesh',
        'phone': '01648735492',
        'email': 'badhandas914@gmail.com',
    }
    from django.shortcuts import render

def contact(request):
    return render(request, 'store/contact.html')

def about(request):
    return render(request, 'store/about.html')

