from django.shortcuts import render

from apps.product.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html',{"newarrivals":products[:12],"hotsales":products[13:25]})

def about(request):
    return render(request, 'aboutUs.html')

def contact(request):
    return render(request, 'contactUs.html')
