from django.urls import path
from . import views

urlpatterns = [
    path('shop/',views.shop,name='shop'),
    path('delete_comment/<int:comment_id>/',views.delete_comment ,name='delete_comment'),
    path('shop/<slug:category_slug>/',views.category,name='category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product, name='product'),
]