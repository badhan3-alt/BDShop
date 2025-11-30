from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product

# Helper to get or create a cart for the logged-in user
def _get_user_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None

# Add product to cart
@login_required
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_user_cart(request)
    if not cart:
        return redirect('store')

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('carts:cart')

# Remove 1 quantity of a product from cart
@login_required
def remove_cart(request, product_id):
    cart = _get_user_cart(request)
    if not cart:
        return redirect('store')

    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('carts:cart')

# Remove entire cart item
@login_required
def remove_cart_item(request, product_id):
    cart = _get_user_cart(request)
    if not cart:
        return redirect('store')

    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('carts:cart')

# Cart view
@login_required
def cart(request):
    cart = _get_user_cart(request)
    cart_items = cart.items.all() if cart else []
    total = sum(item.total_price for item in cart_items) if cart else 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

# Checkout view
@login_required
def checkout(request):
    cart = _get_user_cart(request)
    if not cart:
        return redirect('store')

    cart_items = cart.items.all()
    total = sum(item.total_price for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)
