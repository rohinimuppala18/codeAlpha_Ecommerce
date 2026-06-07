from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Category, Product, Review, Wishlist
from .forms import ReviewForm

def home(request):
    """
    Renders the homepage.
    Displays categories and the latest 8 featured/active products.
    """
    categories = Category.objects.all()[:6]
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    return render(request, 'products/home.html', {
        'categories': categories,
        'products': products,
    })

def product_list(request, category_slug=None):
    """
    Renders the shop listing page with search, category filtering,
    sorting (newest, low-to-high, high-to-low), and pagination.
    """
    category = None
    categories = Category.objects.all()
    products_list = Product.objects.filter(is_active=True)

    # Filter by Category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)

    # Search functionality
    query = request.GET.get('q')
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Sorting functionality
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    else:
        products_list = products_list.order_by('-created_at') # Default is newest

    # Pagination: 9 products per page
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products/shop.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'sort_by': sort_by,
    })

def product_detail(request, id, slug):
    """
    Renders the details of a single product.
    Includes add-to-cart form, list of reviews, review submission form,
    and product recommendations (other products in same category).
    """
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    reviews = product.reviews.all()
    
    # Recommended products (same category, excluding current product, limit 4)
    recommendations = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]

    # Handle review submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to write a review.')
            return redirect('accounts:login')
            
        # Check if user already reviewed this product
        if Review.objects.filter(product=product, user=request.user).exists():
            messages.warning(request, 'You have already reviewed this product.')
            return redirect('products:product_detail', id=product.id, slug=product.slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you! Your review has been submitted.')
            return redirect('products:product_detail', id=product.id, slug=product.slug)
    else:
        form = ReviewForm()

    # Check if item is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        in_wishlist = wishlist.products.filter(id=product.id).exists()

    return render(request, 'products/detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'recommendations': recommendations,
        'in_wishlist': in_wishlist,
    })

@login_required
def toggle_wishlist(request, product_id):
    """
    Toggles a product in the user's wishlist.
    Adds it if not present, removes it if it is.
    Supports AJAX requests.
    """
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    is_added = False
    if wishlist.products.filter(id=product.id).exists():
        wishlist.products.remove(product)
        msg = f'Removed "{product.name}" from your wishlist.'
    else:
        wishlist.products.add(product)
        is_added = True
        msg = f'Added "{product.name}" to your wishlist!'

    # Check if request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == 'true':
        return JsonResponse({
            'success': True,
            'is_added': is_added,
            'message': msg,
            'wishlist_count': wishlist.products.count()
        })

    if is_added:
        messages.success(request, msg)
    else:
        messages.info(request, msg)

    # Redirect back to where user came from, or shop
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'products:shop'
    return redirect(next_url)

@login_required
def wishlist_view(request):
    """
    Renders the logged-in user's wishlist page.
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, 'products/wishlist.html', {
        'products': products
    })

def search_suggestions(request):
    """
    Returns live search suggestions for active products matching the 'q' parameter.
    """
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    products = Product.objects.filter(is_active=True, name__icontains=query)[:5]
    suggestions = []
    for prod in products:
        suggestions.append({
            'name': prod.name,
            'price': float(prod.price),
            'url': reverse('products:product_detail', kwargs={'id': prod.id, 'slug': prod.slug}),
            'category': prod.category.name,
            'image_url': prod.image.url if prod.image else None
        })
    return JsonResponse({'suggestions': suggestions})
