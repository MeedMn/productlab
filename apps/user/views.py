from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect,get_object_or_404
from apps.cart.cart import Cart
from apps.product.models import Product
from .UserFroms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from apps.user.UserFroms import UserForm
from .models import UserModel
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def SignUp_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            all_users = UserModel.objects.all()
            for us in all_users:
                if us.email == user.email:
                    messages.error(request, 'That email is already in use')
                    return redirect('signupuser')
                if us.name == user.username:
                    messages.error(request, 'That username is already in use')
                    return redirect('signupuser')
            login(request, user)
            users = UserModel.objects.create(name=user.username,email=user.email,creator=user)
            messages.success(request, 'Signed up successfully!')
            return redirect('/')
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password != password2:
                messages.error(request, 'Passwords do not match! Try again')
                return redirect('signupuser')
            all_users = UserModel.objects.all()
            for us in all_users:
                if us.email == email:
                    messages.error(request, 'That email is already in use')
                    return redirect('signupuser')
                if us.name == username:
                    messages.error(request, 'That username is already in use')
                    return redirect('signupuser')
            messages.error(request, 'Username/Email invalid')
            return redirect('signupuser')

    form = UserForm()
    return render(request=request, template_name="SignUp_user.html", context={'form':form})


def Login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed in successfully!')
                return redirect("/")
        else:
            messages.error(request,"verify the username and the password")
            return redirect('loginuser')
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="Login_user.html", context={"form":form})

@login_required(login_url='loginuser')
def add_cart(request,id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=id)
    cart.add(product_id=product.id)
    messages.success(request, 'This Product was added to the cart!')
    user1 = UserModel.objects.get(name=request.user.username)
    return redirect('cart')



@login_required(login_url='loginuser')
def wishlist(request):
    if request.method == "GET":
        user1 = UserModel.objects.get(name=request.user.username)
        wishlist = WishList.objects.filter(user=user1)
        page = request.GET.get('page', 1)
        paginator = Paginator(wishlist, 5)
        try:
            wishlist = paginator.page(page)
        except PageNotAnInteger:
            wishlist = paginator.page(1)
        except EmptyPage:
            wishlist = paginator.page(paginator.num_pages)
        return render(request,"wishList.html",{'wishlist':wishlist})
    



@login_required(login_url='loginuser')
def add_wishlist(request,id):
    user1 = UserModel.objects.get(name=request.user.username)
    wishlist = WishList()
    if not WishList.objects.filter(Q(user=user1) & Q(product=Product.objects.get(id=id))):
        wishlist = WishList.objects.create(user=user1, product = Product.objects.get(id=id))
        wishlist.save()
        messages.success(request, 'This Product is in now in your wishlist!')
    return redirect('/'+wishlist.product.category.slug+"/"+wishlist.product.slug)




@login_required(login_url='loginuser')
def delete_wishlist(request,id,redirect_option):
    user1 = UserModel.objects.get(name=request.user.username)
    wishlist = WishList.objects.filter(Q(user=user1) & Q(product = Product.objects.get(id=id)))
    product = Product.objects.get(id=id)
    wishlist.delete()
    if not redirect_option == 1:
        messages.success(request, 'That Product has been removed from your wishlist')
        return redirect('wishlist')
    else:
        messages.success(request, 'This Product has been removed from your wishlist')
        return redirect('/'+product.category.slug+'/'+product.slug)