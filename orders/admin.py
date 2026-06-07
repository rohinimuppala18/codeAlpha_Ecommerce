from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'total_price', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    list_editable = ('status', 'is_paid')
    inlines = [OrderItemInline]
    search_fields = ('id', 'first_name', 'last_name', 'email')
