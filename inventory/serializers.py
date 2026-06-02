from rest_framework import serializers
from inventory.models import Products, Branch, Inventory


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category', 'created_at']


class BranchSerializer(serializers.ModelSerializer):
    stock_manager = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'stock_manager', 'branch_name', 'location', 'created_at']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'branch', 'quantity', 'last_updated']
