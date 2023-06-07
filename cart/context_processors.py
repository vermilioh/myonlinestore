from .cart import Cart


def cart(request):
    current_cart = Cart(request)
    total_items = sum(item['quantity'] for item in current_cart)
    return {'cart_total_items': total_items}

