from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from store.models import Product
from category.models import Category  # Your category model
from django.http import HttpResponse
from django.db.models import Q
def store(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filtering by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'store/store.html', {
        'products': products,
        'categories': categories
    })
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {
        'product': product
    })

def search(request):
    keyword = request.GET.get('keyword')  # get the search term from the form
    products = []

    if keyword:  # if user entered something
        products = Product.objects.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)| Q(description__icontains=product_detail),
            available=True
        )
        product_count=products.count()
    categories = Category.objects.all()
    context = {
        'products': products,
        'keyword': keyword,
        'Category':Category,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)