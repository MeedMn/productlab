from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('signupuser/', views.SignUp_user, name='signupuser'),
    path('add_cart/<int:id>/',views.add_cart ,name='add_cart'),
    path('loginuser/',views.Login_user,name='loginuser'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='Login_user.html'),name='login'),
]