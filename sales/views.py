from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from sales.models import Order, PurchaseOrder, Distribution, Sales, CartItem
from sales.serializers import (
    OrderSerializer, PurchaseOrderSerializer, PurchaseOrderStatusSerializer,
    DistributionSerializer, SalesSerializer, CartItemSerializer
)
from inventory.models import Inventory


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        purchase_order = self.get_object()
        serializer = PurchaseOrderStatusSerializer(purchase_order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']

        # farmer can only accept or reject
        if new_status in [PurchaseOrder.ACCEPTED, PurchaseOrder.REJECTED]:
            if request.user != purchase_order.farmer:
                return Response({'error': 'Only the farmer can accept or reject.'}, status=status.HTTP_403_FORBIDDEN)

        # only admin can move to In Transit
        if new_status == PurchaseOrder.IN_TRANSIT:
            if request.user != purchase_order.admin:
                return Response({'error': 'Only the admin can mark as In Transit.'}, status=status.HTTP_403_FORBIDDEN)

        # admin confirms delivery — inventory increases
        if new_status == PurchaseOrder.DELIVERED:
            if request.user != purchase_order.admin:
                return Response({'error': 'Only the admin can confirm delivery.'}, status=status.HTTP_403_FORBIDDEN)
            inventory, created = Inventory.objects.get_or_create(
                product=purchase_order.product,
                branch=None,
                defaults={'quantity': 0}
            )
            inventory.quantity += purchase_order.quantity
            inventory.save()

        serializer.save()
        return Response(serializer.data)


class DistributionViewSet(viewsets.ModelViewSet):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        branch = serializer.validated_data['branch']
        quantity = serializer.validated_data['quantity']

        try:
            main_inventory = Inventory.objects.get(product=product, branch=None)
        except Inventory.DoesNotExist:
            raise ValidationError('No inventory found for this product.')

        if main_inventory.quantity < quantity:
            raise ValidationError(f'Not enough stock. Available: {main_inventory.quantity}')

        # decrease main inventory
        main_inventory.quantity -= quantity
        main_inventory.save()

        # increase branch inventory
        branch_inventory, _ = Inventory.objects.get_or_create(
            product=product,
            branch=branch,
            defaults={'quantity': 0}
        )
        branch_inventory.quantity += quantity
        branch_inventory.save()

        serializer.save(admin=self.request.user)


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
