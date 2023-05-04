from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .cart import Cart
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.user.models import UserModel
# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        messages.success(request, 'That artwork was removed from the cart')
        return redirect('cart')
    return render(request, 'cart.html', {})