from rest_framework import serializers
from sales.models import Order, Sales, CartItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'product', 'quantity', 'total_price', 'status', 'order_date']


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['id', 'user', 'product', 'sale_date', 'amount']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'customer', 'product', 'quantity', 'added_at']
