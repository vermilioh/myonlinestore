from _decimal import Decimal
import copy
from django.conf import settings
from shop.models import Product
from .models import CartItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        print(f"Adding product {product.id} to cart")
        product_id = str(product.id)
        if product_id in self.cart:
            print(f"Product {product_id} not in cart, adding")
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': float(product.price)}
        self.save()

    def save(self):
        # update the session cart
        self.session['cart'] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['price'] = str(product.price)  # use product's price
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self)

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # Удалите корзину из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_item_total(self, item):
        return item['price'] * item['quantity']

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()
