from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from carts.models import Cart

def store(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    keyword = request.GET.get('keyword')
    products = []
    product_count = 0

    if keyword:
        products = Product.objects.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(short_description__icontains=keyword),
            available=True
        )
        product_count = products.count()

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)

@login_required(login_url='login')
def checkout(request):
    # Get user cart, if exists
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('store')

    cart_items = cart.items.all()  # related_name should be "items"
    total = sum(item.total_price for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'orders/checkout.html', context)


