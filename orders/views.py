from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Payment, OrderProduct
from carts.models import Cart, CartItem
from carts.models import Cart, CartItem
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
from carts.models import Cart, CartItem


def checkout(request):
    
    return render(request, 'orders/checkout.html')

def payment(request):
    
    return render(request, 'orders/payment.html')

def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_success.html', {'order': order})

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    return render(request, 'orders/order_detail.html', {'order': order, 'order_products': order_products})

def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            return redirect('orders:payment')
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {'form': form})

def dashboard_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard/orders.html', {'orders': orders})

