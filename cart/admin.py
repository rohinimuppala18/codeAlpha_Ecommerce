from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'total_items', 'total_price')
    list_filter = ('created_at', 'user')
    inlines = [CartItemInline]
    search_fields = ('user__username', 'session_key')
