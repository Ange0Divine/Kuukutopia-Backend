from django.contrib import admin
from inventory.models import Products, Branch, Inventory

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'quantity', 'created_at']
    list_filter = ['category']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch_name', 'location', 'created_at']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'branch', 'quantity', 'last_updated']
