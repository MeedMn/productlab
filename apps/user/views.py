from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect,get_object_or_404
from .UserFroms import *
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from apps.user.UserFroms import UserForm
from .models import UserModel

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
                    return redirect('SignUp_user')
                if us.name == user.username:
                    messages.error(request, 'That username is already in use')
                    return redirect('SignUp_user')
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
                return redirect('SignUp_user')
            all_users = UserModel.objects.all()
            for us in all_users:
                if us.email == email:
                    messages.error(request, 'That email is already in use')
                    return redirect('SignUp_user')
                if us.name == username:
                    messages.error(request, 'That username is already in use')
                    return redirect('SignUp_user')
            messages.error(request, 'Username/Email invalid')
            return redirect('SignUp_user')

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
            return redirect('Login_user')
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="Login_user.html", context={"form":form})