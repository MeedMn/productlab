import math
import random
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from apps.product.models import Category, Comment, Product
from django.db.models import Max
from django.db.models import Q

# Create your views here.

def delete_comment(request,comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])

def product(request,category_slug,product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    relatedProducts = random.sample(list(Product.objects.filter(category__slug=category_slug)),4)
    comments = Comment.objects.all().filter(product=product)
    if request.method == 'GET' and request.GET.get('commentbtn'):
        comment_text = request.GET.get('comment')
        User = request.user.username
        comment = Comment.objects.create(product=product,user1=User,content=comment_text)
        comment.save()
        return HttpResponseRedirect(reverse('product', args=(category_slug,product_slug,)))
    return render(request, 'product.html',{'product':product,'comments':comments,'relatedProducts':relatedProducts})

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
    return render(request,'shop.html',{'products':products,"categoryTitle":category.title})

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
        
    return render(request,'shop.html',{"products":products,'max':max,'categoryTitle':"All"})

def search(request):
    query = request.GET.get('query','')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query) | Q(seller__name__icontains=query))
    sort_by = request.GET.get('sort_by', None)
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
    page2 = request.GET.get('page2', 1)
    paginator = Paginator(products, 12)
    try:
        products = paginator.page(page2)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,'search.html',{'products':products, 'query':query})

