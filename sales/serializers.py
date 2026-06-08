from rest_framework import serializers
from sales.models import Order, PurchaseOrder, Distribution, Sales, CartItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'product', 'quantity', 'total_price', 'status', 'order_date']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'admin', 'farmer', 'product', 'quantity', 'total_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['admin', 'status', 'created_at', 'updated_at']


class PurchaseOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['status']


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = ['id', 'admin', 'product', 'branch', 'quantity', 'distributed_at']
        read_only_fields = ['admin', 'distributed_at']


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['id', 'user', 'product', 'sale_date', 'amount']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'customer', 'product', 'quantity', 'added_at']
