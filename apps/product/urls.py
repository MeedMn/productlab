from django.urls import path
from . import views

urlpatterns = [
    path('shop/',views.shop,name='shop'),
    path('shop/<slug:category_slug>/',views.category,name='category')
]