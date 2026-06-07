from .models import Cart, CartItem

def get_cart_for_request(request):
    """
    Retrieves or creates the cart for the current request.
    Handles merging of a guest session-based cart into the authenticated user's cart.
    """
    if request.user.is_authenticated:
        # Get or create cart for the logged-in user
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if there is an anonymous session cart to merge
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            try:
                session_cart = Cart.objects.get(id=session_cart_id)
                # Merge session items into user cart
                for item in session_cart.items.all():
                    user_item, item_created = CartItem.objects.get_or_create(
                        cart=user_cart, 
                        product=item.product
                    )
                    if not item_created:
                        user_item.quantity += item.quantity
                    else:
                        user_item.quantity = item.quantity
                    user_item.save()
                
                # Delete the temporary session cart
                session_cart.delete()
                del request.session['cart_id']
            except Cart.DoesNotExist:
                pass
                
        return user_cart
    else:
        # User is anonymous. Retreive from session cart ID or session key.
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            try:
                cart = Cart.objects.get(id=session_cart_id)
                return cart
            except Cart.DoesNotExist:
                pass

        # Create session if not exists
        if not request.session.session_key:
            request.session.create()

        # Create new cart for guest user
        cart = Cart.objects.create(session_key=request.session.session_key)
        request.session['cart_id'] = cart.id
        return cart
