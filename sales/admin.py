from django.contrib import admin
from sales.models import Order, Sales, CartItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'total_price', 'status', 'order_date']
    list_filter = ['status']

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'amount', 'sale_date']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'added_at']
