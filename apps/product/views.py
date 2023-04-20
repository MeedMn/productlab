import math
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.product.models import Category, Product
from django.db.models import Max

# Create your views here.

def shop(request):
    categories = Category.objects.all()
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
        
    return render(request,'shop.html',{"categories":categories,"products":products,'max':max})