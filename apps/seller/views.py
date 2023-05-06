import os
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from apps.product.ProductForms import *
from apps.product.models import Product, ProductImage
from apps.user.UserFroms import *
from .models import Seller
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

# Create your views here.
def SignUp_seller(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            all_sellers = Seller.objects.all()
            for us in all_sellers:
                if us.email == user.email:
                    messages.error(request, 'That email is already in use')
                    return redirect('SignUp_seller')
                if us.name == user.username:
                    messages.error(request, 'That username is already in use')
                    return redirect('SignUp_seller')
            login(request, user)
            users = Seller.objects.create(name=user.username,email=user.email,creator=user)
            messages.success(request, 'Signed up successfully!')
            return redirect('/')
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password != password2:
                messages.error(request, 'Passwords do not match! Try again')
                return redirect('SignUp_seller')
            all_sellers = Seller.objects.all()
            for us in all_sellers:
                if us.email == email:
                    messages.error(request, 'That email is already in use')
                    return redirect('SignUp_seller')
                if us.name == username:
                    messages.error(request, 'That username is already in use')
                    return redirect('SignUp_seller')
            messages.error(request, 'Username/Email invalid')
            return redirect('SignUp_seller')

    form = UserForm()
    return render(request=request, template_name="SignUp_seller.html", context={'form':form})


def Login_seller(request):
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
            return redirect('Login_seller')
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="Login_seller.html", context={"form":form})

@login_required(login_url='Login_seller')
def dashboard(request):
    seller = request.user.seller
    products = seller.products.all().order_by("-date_added")
    return render(request,"Dashboard.html",{"seller":seller,"products":products})

@login_required(login_url='Login_seller')
def add_product(request):
    if request.method == 'POST':
        form = ProductForms(request.POST, request.FILES)
        more_images = ProductImageForm(request.POST, request.FILES)
        if (form.is_valid() and more_images.is_valid()) or form.is_valid():
            if float(request.POST.get('price')) < 10000 and float(request.POST.get('price')) > 0 :
                products = Product.objects.all()
                product = form.save(commit=False)
                for existing in products:
                    if product.title == existing.title:
                        messages.success(request, 'That title is already taken!')
                        return redirect('add_product')
                product.seller = request.user.seller
                product.slug = slugify(product.title)
                product.generate_ref()
                product.save()
                images = request.FILES.getlist('more_images')
                if images:
                    for image in images:
                        image = ProductImage(image=image, product=product)
                        image.save()
                messages.success(request, 'Your Product is now pending review!')
            else:
                messages.error(request,"The price must be between €1 and €9999!")
                return render(request,'add_product.html',{'form':form,'more_images':more_images})
            return redirect('dashboard')
    else:
        form = ProductForms()
        more_images = ProductImageForm()
    return render(request,'add_product.html',{'form':form,'more_images':more_images})


@login_required(login_url='Login_seller')
def updateProduct(request,primaryKey):
    getProduct = get_object_or_404(Product,pk=primaryKey)
    try:
        os.remove("C:/Users/Snof_Bo/Desktop/Enviroment_Python/productlab/media/uploads/"+getProduct.image.name)
        os.remove("C:/Users/Snof_Bo/Desktop/Enviroment_Python/productlab/media/"+getProduct.image.name)
    except Exception as error :
        print(error)
        pass
    if request.method == 'POST':
        form = ProductForms(request.POST, request.FILES,instance=getProduct)
        more_images = ProductImageForm(request.POST, request.FILES)
        if (form.is_valid() and more_images.is_valid()) or form.is_valid():
            if float(request.POST.get('price')) < 10000 and float(request.POST.get('price')) > 0 : 
                product = form.save(commit=False)
                img_to_delete = request.POST.getlist('delete')
                for image in img_to_delete:
                    print(image)
                    ProductImage.objects.filter(image=image).delete()
                product.image = request.FILES['image']
                product.thumbnail = request.FILES['image']
                product.seller = request.user.seller
                product.slug = slugify(product.title)
                product.generate_ref()
                product.save()
                images = request.FILES.getlist('more_images')
                if images:
                    for image in images:
                        image = ProductImage(image=image, product=product)
                        image.save()
                messages.success(request, 'Your Product is now pending review!')
            else:
                messages.error(request,"The price must be between €1 and €9999!")
                return render(request,'updateProduct.html',{'form':form,'more_images':more_images})
            return redirect('dashboard')
    else:
        form = ProductForms(instance=getProduct)
        more_images = ProductImageForm()
    return render(request,'updateProduct.html',{'form':form,'more_images':more_images})

@login_required(login_url='Login_seller')
def deleteProduct(request , primaryKey):
    getProductToDelete = get_object_or_404(Product,pk=primaryKey)
    try:
        os.remove("C:/Users/Snof_Bo/Desktop/Enviroment_Python/productlab/media/uploads/"+getProductToDelete.image.name)
        os.remove("C:/Users/Snof_Bo/Desktop/Enviroment_Python/productlab/media/"+getProductToDelete.image.name)
    except Exception as error :
        print(error)
        pass
    getProductToDelete.delete()
    return redirect('dashboard')