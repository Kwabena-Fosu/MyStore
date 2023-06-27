import random
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db.models import Q

from .models import Product, Testimonial
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def home(request):

    featured = Product.objects.get(id=10)

    total_products = Product.objects.count()
    total_testimonials = Testimonial.objects.count()

    #number of random objects to fetch
    num_products = 6
    num_testimonials = 4

    # Generate a random list of indices within the range of the total products
    random_indices_p = random.sample(range(total_products), num_products)
    random_indices_t = random.sample(range(total_testimonials), num_testimonials)

    # Fetching the random objects using the indices
    random_products = Product.objects.filter(pk__in=random_indices_p)
    random_testimonials = Testimonial.objects.filter(pk__in=random_indices_t)

    context = {
        'random_products': random_products, 
        'random_testimonials' : random_testimonials,  
        'featured' : featured,     
    }

    return render(request, 'store/home.html', context)

def store(request, category_slug=None):
    products = None
    categories = None

    if category_slug != None:
        categories = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('-created_date')
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)