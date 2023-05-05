from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/',views.about,name = 'about'),
    path('contact/',views.contact,name = 'contact'),
    path('newsletter/',views.newsletter,name = 'newsletter'),
    path('delete_newsletter/',views.delete_newsletter,name = 'delete_newsletter'),
]