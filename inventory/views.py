from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, BasePermission
from accounts.views import IsAdmin
from inventory.models import Products, Branch, Inventory
from inventory.serializers import ProductsSerializer, ProductStatusSerializer, BranchSerializer, InventorySerializer
from accounts.models import StockManager


class IsNotCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != 'Customer'


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsNotCustomer]

    def get_queryset(self):
        queryset = Products.objects.all()
        status_filter = self.request.query_params.get('status')
        created_by = self.request.query_params.get('created_by')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if created_by:
            queryset = queryset.filter(created_by__id=created_by)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], url_path='update-status', permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        product = self.get_object()
        serializer = ProductStatusSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['get'], url_path='stock', permission_classes=[IsAuthenticated])
    def stock(self, request, pk=None):
        branch = self.get_object()
        inventory = Inventory.objects.filter(branch=branch)
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='assign-manager')
    def assign_manager(self, request, pk=None):
        branch = self.get_object()
        stock_manager_id = request.data.get('stock_manager_id')
        if not stock_manager_id:
            return Response({'error': 'stock_manager_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            stock_manager = StockManager.objects.get(id=stock_manager_id)
        except StockManager.DoesNotExist:
            return Response({'error': 'Stock manager not found.'}, status=status.HTTP_404_NOT_FOUND)
        branch.stock_Manager = stock_manager
        branch.save()
        return Response(BranchSerializer(branch).data)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
