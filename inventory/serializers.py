from rest_framework import serializers
from inventory.models import Products, Branch, Inventory


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'image', 'price', 'quantity', 'unit', 'category', 'status', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'status', 'created_at']


class ProductStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['status']


class BranchSerializer(serializers.ModelSerializer):
    stock_manager_username = serializers.CharField(write_only=True)
    stock_Manager = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'stock_Manager', 'stock_manager_username', 'branch_name', 'location', 'created_at']

    def validate_stock_manager_username(self, value):
        from accounts.models import StockManager, User
        try:
            user = User.objects.get(username=value)
            stock_manager = StockManager.objects.get(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user with this username.')
        except StockManager.DoesNotExist:
            raise serializers.ValidationError('This user is not a stock manager.')
        return stock_manager

    def create(self, validated_data):
        stock_manager = validated_data.pop('stock_manager_username')
        return Branch.objects.create(stock_Manager=stock_manager, **validated_data)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'branch', 'quantity', 'last_updated']
