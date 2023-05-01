from django.shortcuts import render

from apps.product.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    newarrivals = Product.objects.all().order_by('-date_added')[:12]
    return render(request, 'index.html',{"newarrivals":newarrivals,"hotsales":products[13:25]})

def about(request):
    return render(request, 'aboutUs.html')

def contact(request):
    return render(request, 'contactUs.html')
