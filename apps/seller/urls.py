from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('SignUp_seller/', views.SignUp_seller, name='SignUp_seller'),
    path('Login_seller/',views.Login_seller,name='Login_seller'),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='Login_seller.html'),name='login'),
]