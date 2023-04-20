from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.product.models import Category, Product

# Create your views here.

def shop(request):
    categories = Category.objects.all()
    products1 = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products1, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    return render(request,'shop.html',{"categories":categories,"products":products})