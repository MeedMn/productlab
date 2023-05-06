from .models import NewsLetter

def newsletter(request):
    a = NewsLetter.objects
    if request.user.is_authenticated:
        a = a.filter(email=request.user.email).exists
    else:
        a = False
    return {'newsletter':a}