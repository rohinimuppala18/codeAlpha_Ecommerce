from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Cart Model linked either to a User (if logged in) or a Session (if guest)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Cart for User: {self.user.username}"
        return f"Guest Cart: {self.session_key}"

    @property
    def total_price(self):
        """Calculates the sum of all item subtotals in the cart."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Calculates the sum of all item quantities in the cart."""
        return sum(item.quantity for item in self.items.all())


# CartItem Model connecting specific products to a Cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        """Calculates subtotal for this cart line item."""
        return self.product.price * self.quantity
