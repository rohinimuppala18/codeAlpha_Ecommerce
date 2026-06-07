from .utils import get_cart_for_request

def cart_total(request):
    """
    Django context processor to make the cart and its totals 
    available to all templates dynamically.
    """
    cart = get_cart_for_request(request)
    return {
        'cart': cart,
        'cart_total_items': cart.total_items,
        'cart_total_price': cart.total_price,
    }
