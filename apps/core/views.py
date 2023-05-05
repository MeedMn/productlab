from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render,redirect
from django.contrib import messages
from apps.product.models import Product
from apps.core.models import NewsLetter
# Create your views here.
def index(request):
    products = Product.objects.all()
    newarrivals = Product.objects.all().order_by('-date_added')[:12]
    return render(request, 'index.html',{"newarrivals":newarrivals,"hotsales":products[13:25]})

def about(request):
    return render(request, 'aboutUs.html')

def contact(request):
    if request.method == "POST" and request.POST.get('contact'):
        from_email = settings.DEFAULT_EMAIL_FROM
        to_email = 'productlab010@gmail.com'
        subject = request.POST.get('subject')
        text_content = 'Full name: '+str(request.POST.get('name'))+'\nEmail: '+str(request.POST.get('email'))+'\nMessage: '+str(request.POST.get('message'))
        msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=[to_email])
        msg.send()
        messages.success(request, 'Successfully sent!')
    return render(request, 'contactUs.html')


def newsletter(request):
    news = NewsLetter.objects.create(email=request.user.email)
    news.save()
    messages.success(request, "You're now subscribed to the newsletter!")
    return redirect(request.META['HTTP_REFERER'])
    
def delete_newsletter(request):
    news = NewsLetter.objects.get(email=request.user.email)
    news.delete()
    messages.success(request, "You're now unsubscribed from the newsletter!")
    return redirect(request.META['HTTP_REFERER'])