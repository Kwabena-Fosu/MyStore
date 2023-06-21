import random
from django.shortcuts import render, get_object_or_404
from .models import Product, Testimonial
from category.models import Category

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
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()


    context = {
        'products': products,
        'categories': categories,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }

    return render(request, 'store/product_detail.html', context)