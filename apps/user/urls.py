from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('signupuser/', views.SignUp_user, name='signupuser'),
    path('add_cart/<int:id>/',views.add_cart ,name='add_cart'),
    path('loginuser/',views.Login_user,name='loginuser'),
     path('wishlist/',views.wishlist,name = 'wishlist'),
    path('<int:id>', views.add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<int:id>/<int:redirect_option>',views.delete_wishlist ,name='delete_wishlist'),
    path('account_settings/',views.account_settings,name = 'account_settings'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='Login_user.html'),name='login'),
]