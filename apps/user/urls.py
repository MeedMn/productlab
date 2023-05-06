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
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password_reset_form.html",success_url= reverse_lazy ("password_reset_done"),extra_email_context={'domain':'127.0.0.1:8000','site_name':"ProductLab"}),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url= reverse_lazy ("loginuser")),name='password_reset_confirm'),
]