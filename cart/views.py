from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem
from .utils import get_cart_for_request

def cart_detail(request):
    """
    Renders the current contents of the user's shopping cart.
    """
    cart = get_cart_for_request(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """
    Adds a product to the cart or increases its quantity.
    Validates product stock before adding. Supports AJAX JSON responses.
    """
    cart = get_cart_for_request(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Retrieve quantity from POST, default is 1
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
        
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Calculate target quantity
    if created:
        target_qty = quantity
    else:
        target_qty = cart_item.quantity + quantity
        
    # Stock level check
    if target_qty > product.stock:
        error_msg = f'Cannot add item. Only {product.stock} items in stock.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': error_msg})
            
        messages.warning(request, error_msg)
        if created:
            cart_item.delete()
        return redirect('products:product_detail', id=product.id, slug=product.slug)

    cart_item.quantity = target_qty
    cart_item.save()
    
    success_msg = f'Added "{product.name}" to your cart!'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': success_msg,
            'total_items': cart.total_items,
            'total_price': float(cart.total_price)
        })

    messages.success(request, success_msg)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """
    Updates the quantity of an item in the cart.
    Validates product stock. If quantity is 0, removes the item.
    """
    cart = get_cart_for_request(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        cart_item.delete()
        messages.info(request, f'Removed "{product.name}" from your cart.')
    else:
        if quantity > product.stock:
            messages.warning(request, f'Only {product.stock} units of "{product.name}" are available in stock.')
            return redirect('cart:cart_detail')
            
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Updated quantity for "{product.name}".')

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """
    Removes a product from the shopping cart.
    """
    cart = get_cart_for_request(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    
    messages.info(request, f'Removed "{product.name}" from your cart.')
    return redirect('cart:cart_detail')
