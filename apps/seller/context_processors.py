from .models import Seller

def sellers(request):
    seller = Seller.objects.all()
    return {'sellers':seller}