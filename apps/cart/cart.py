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
            item['total_price'] = item['product'].price

            yield item
    def __len__(self):
        c = 0
        for item in self.cart.values():
            c +=1
        return c
        
    def add(self, product_id):
        product_id = str(product_id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {'id': product_id}
                        
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

        return sum(item['product'].price for item in self.cart.values())

    def get_final_cost(self):
        total_cost = self.get_total_cost()
        final_cost = float(total_cost) + float(total_cost)*(5/100)
        return final_cost