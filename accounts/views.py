from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from orders.models import Order

def register(request):
    """
    Handles user registration.
    Validates form data and creates a user (with an automatic profile via signals).
    """
    if request.user.is_authenticated:
        return redirect('products:home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handles user login using Django's Authentication System.
    Redirects user to requested next URL or dashboard on success.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Check for redirect parameter
                next_url = request.GET.get('next') or 'accounts:dashboard'
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handles user logout.
    Clears the session and redirects to home.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('products:home')


@login_required
def dashboard(request):
    """
    Renders the user's dashboard.
    Handles updating user and profile details, and displays order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_spend = sum(order.total_price for order in orders)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile details have been updated!')
            return redirect('accounts:dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/dashboard.html', {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders,
        'total_spend': total_spend,
    })
