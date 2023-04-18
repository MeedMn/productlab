from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('SignUp_user/', views.SignUp_user, name='SignUp_user'),
    path('Login_user/',views.Login_user,name='Login_user'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='Login_user.html'),name='login'),
]