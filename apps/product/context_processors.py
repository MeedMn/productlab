from apps.product.models import Category

def menu_categories(request):
    categories = Category.objects.order_by('title')
    return {'categories':categories}