import math
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.product.models import Category, Product
from django.db.models import Max

# Create your views here.

def category(request,category_slug):
    category = get_object_or_404(Category,slug=category_slug)
    products = category.products.all()
    max = math.ceil(category.products.aggregate(price=Max('price'))['price'])
    price_range = request.GET.get('price_range', max)
    products = products.filter(price__range=(0, price_range))
    sort_by = request.GET.get('sort_by', None)
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')    
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,'shop.html',{'products':products})

def shop(request):
    products = Product.objects.all()
    max = math.ceil(Product.objects.aggregate(price=Max('price'))['price'])
    
    price_range = request.GET.get('price_range', max)
    products = products.filter(price__range=(0, price_range))
    sort_by = request.GET.get('sort_by', None)
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    return render(request,'shop.html',{"products":products,'max':max})