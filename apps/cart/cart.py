from django.conf import settings
from apps.product.models import Product

from django.conf import settings
from apps.product.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def __len__(self):
        c = 0
        for item in self.cart.values():
            c += item['quantity']
        return c
        
    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart and self.cart[product_id]['quantity'] <= Product.objects.filter(id=product_id):
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'id': product_id, 'quantity': quantity}
        self.save()
    
    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['product'].price * item['quantity'] for item in self.cart.values())

    def get_final_cost(self):
        total_cost = self.get_total_cost()
        final_cost = float(total_cost) + float(total_cost)*(5/100)
        return final_cost