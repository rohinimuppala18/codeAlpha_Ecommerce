from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.utils import get_cart_for_request
from .models import Order, OrderItem
from .forms import OrderCreateForm
from products.models import Product

def order_create(request):
    """
    Handles checkout and order creation.
    Pre-fills forms for authenticated users, saves the order details,
    decrements stock, and clears the user's cart.
    """
    cart = get_cart_for_request(request)
    
    # Redirect if cart is empty
    if cart.total_items == 0:
        messages.warning(request, 'Your cart is empty. Add some products before checking out.')
        return redirect('products:shop')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            order.total_price = cart.total_price
            order.save()

            # Create order items and decrement product stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Decrement inventory stock
                product = item.product
                product.stock = max(0, product.stock - item.quantity)
                product.save()

            # Clear cart items after successful order creation
            cart.items.all().delete()
            
            # Store order ID in session for success view validation
            request.session['last_order_id'] = order.id
            messages.success(request, 'Order placed successfully!')
            return redirect('orders:order_success', order_id=order.id)
    else:
        # Pre-fill form if user is authenticated and has a profile
        initial_data = {}
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            if profile:
                initial_data.update({
                    'address': profile.address,
                    'city': profile.city,
                    'state': profile.state,
                    'postal_code': profile.postal_code,
                    'country': profile.country,
                })
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form
    })


def order_success(request, order_id):
    """
    Renders the order success/confirmation page.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})


@login_required
def order_history(request):
    """
    Lists order history for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})
