from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
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

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
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


def add_to_cart(request):
    product_id = str(request.GET['id'])
    cart_product = {product_id: {
        'name': request.GET['name'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['img'],
    }}

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[product_id]['qty'] = int(cart_product[product_id]['qty'])
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse(
        {"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})


def calc_cart_total_price(cart_data):
    cart_total_amount = 0
    for product_id, item in cart_data.items():
        price = float(item['price'])
        qty = int(item['qty'])
        cart_total_amount += price * qty
    return cart_total_amount


def calc_tax(total):
    tax = (2 * total) / 100
    grand_total = total + tax
    return tax, grand_total


def cart_view(request):
    context = {}
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        print()
        cart_total_amount = calc_cart_total_price(cart_data)

        tax, grand_total = calc_tax(cart_total_amount)

        context = {
            'cart_data': cart_data,
            'cart_total_amount': cart_total_amount,
            'totalcartitems': len(cart_data),
            'tax': tax,
            'grand_total': grand_total,
        }
        print(f'context>>>>{context}')
    return render(request, 'store/cart.html', context)


def delete_cart_item(request):
    product_id = request.GET.get('pid')

    # Check if the key exists before deleting
    if 'cart_data_obj' in request.session:
        cart_data_obj = request.session['cart_data_obj']
        if product_id in cart_data_obj:
            del cart_data_obj[product_id]
            request.session['cart_data_obj'] = cart_data_obj

    return redirect('cart')


def update_cart_item_qty(request):
    product_id = str(request.GET['id'])
    product_qty = str(request.GET['qty'])
    cart_data = request.session['cart_data_obj']
    cart_data[product_id]['qty'] = product_qty
    request.session['cart_data_obj'] = cart_data
    return JsonResponse({"data": request.session['cart_data_obj']})


def search_view(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            product_count = products.count()

            context = {
                'products': products,
                'product_count': product_count,

            }

            return render(request, 'store/store.html', context)
    return redirect('store')