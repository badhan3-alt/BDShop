from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderForm  # make sure your form class is OrderForm (PascalCase)
from .models import Order, OrderProduct, Payment
from carts.models import Cart, CartItem
import datetime

@login_required
def place_order(request):
    current_user = request.user
    # Get the cart for the user
    cart = get_object_or_404(Cart, user=current_user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        return redirect('store')

    total = sum(item.product.price * item.quantity for item in cart_items)
    tax = 0
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address_line_1 = form.cleaned_data['address_line_1']
            order.address_line_2 = form.cleaned_data['address_line_2']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.order_note = form.cleaned_data['order_note']
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()

            # Generate order number: YYYYMMDD + order.id
            today = datetime.date.today().strftime("%Y%m%d")
            order_number = today + str(order.id)
            order.order_number = order_number
            order.save()

            # Redirect to payment page
            return redirect('orders:Payment', order_number=order_number)

    return redirect('carts:checkout')



@login_required
def Payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/payment.html', context)


from django.shortcuts import render, redirect
from carts.models import CartItem, Cart

def checkout(request):
    current_user = request.user

    cart_items = []

    # Authenticated user
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=current_user).first()
        if not cart:
            return redirect('store')
        cart_items = CartItem.objects.filter(cart=cart)

    # Anonymous user (using session cart_id)
    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            return redirect('store')
        cart_items = CartItem.objects.filter(cart__cart_id=cart_id)

    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)
