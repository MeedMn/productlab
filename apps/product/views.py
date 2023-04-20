from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.product.models import Category, Product

# Create your views here.

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
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
        
    return render(request,'shop.html',{"categories":categories,"products":products})