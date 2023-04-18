from django.shortcuts import render

from apps.product.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()[:12]
    return render(request, 'index.html',{"products":products})

def about(request):
    return render(request, 'aboutUs.html')

def contact(request):
    return render(request, 'contactUs.html')
