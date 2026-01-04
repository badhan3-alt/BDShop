from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from carts.models import Cart, CartItem
import datetime

@login_required
def place_order(request):
    current_user = request.user
    cart = get_object_or_404(Cart, user=current_user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        return redirect('orders:store')

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

            today = datetime.date.today().strftime("%Y%m%d")
            order_number = today + str(order.id)
            order.order_number = order_number
            order.save()

            
            return redirect('orders:payment', order_number=order_number)

    return redirect('carts:checkout')


@login_required
def payment_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        payment_success = True

        if payment_success:
            CartItem.objects.filter(cart=cart).delete()
            order.status = "Completed"
            order.save()

            return redirect('orders:order_complete', order_number=order.order_number)

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/payment.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from store.models import Product

def checkout(request):
    current_user = request.user
    cart_items = []

    product_id = request.GET.get('product_id')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=current_user).first()
        if not cart:
            cart = Cart.objects.create(user=current_user)

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

        cart_items = CartItem.objects.filter(cart=cart)

    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Cart.objects.create(cart_id=str(product_id or 'guest'))
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(cart_id=cart_id)

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

        cart_items = CartItem.objects.filter(cart__cart_id=cart.id)

    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)



from .models import Order, Payment
from django.contrib.auth.decorators import login_required

@login_required
def cod_order(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        order = get_object_or_404(Order, order_number=order_number, user=request.user)

        payment = Payment.objects.create(
            payment_id=f"COD-{order.order_number}",
            payment_method="COD",
            amount_paid=order.order_total,
            status="Pending"
        )

        order.payment = payment
        order.status = "Completed"
        order.is_ordered = True
        order.save()

        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart).delete()

        return redirect('orders:order_complete', order_number=order.order_number)
    
    else:
        return redirect('store:store')



@login_required
def process_bkash(request):
    if request.method == 'POST':
        trx_id = request.POST.get('trx_id')
        order_number = request.POST.get('order_number')

        order = get_object_or_404(Order, order_number=order_number, user=request.user)

        payment = Payment.objects.create(
            payment_id=trx_id,
            payment_method='bKash',
            amount_paid=order.order_total,
            status='Completed'
        )

        order.payment = payment
        order.status = 'Completed'
        order.is_ordered = True
        order.save()

        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart).delete()

        return redirect('orders:order_complete', order_number=order.order_number)

    else:
        return redirect('store:store')


@login_required
def order_complete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_complete.html', {'order': order})




