from django.shortcuts import render

from apps.product.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    newarrivals = Product.objects.all().order_by('-date_added')[:12]
    return render(request, 'index.html',{"newarrivals":newarrivals,"hotsales":products[13:25]})

def about(request):
    return render(request, 'aboutUs.html')

def contact(request):
    if request.method == "POST" and request.POST.get('contact') : 
        from_email = settings.DEFAULT_EMAIL_FROM
        to_email = 'productlab010@gmail.com'
        subject = request.POST.get('subject')
        text_content = 'Full name: '+str(request.POST.get('name'))+'\nEmail: '+str(request.POST.get('email'))+'\nMessage: '+str(request.POST.get('message'))
        msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=[to_email])
        msg.send()
        messages.success(request, 'Successfully sent!')
    return render(request, 'contactUs.html')
