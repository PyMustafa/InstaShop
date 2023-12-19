from django.shortcuts import render, get_object_or_404

from store.models import Product, Category


# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)


def store(request, category_slug=None):
    products = None
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug=None, product_slug=None):
    try:
        product = Product.objects.get(slug=product_slug, category__slug=category_slug)
    except Exception as e:
        raise e
    context = {
        'product': product,
    }
    return render(request, 'store/product-details.html', context)
