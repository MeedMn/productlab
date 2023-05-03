from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from apps.user.UserFroms import *
from .models import Seller
from django.contrib.auth.decorators import login_required

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