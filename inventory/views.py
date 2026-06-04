from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, BasePermission
from inventory.models import Products, Branch, Inventory
from inventory.serializers import ProductsSerializer, BranchSerializer, InventorySerializer


class IsNotCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != 'Customer'


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsNotCustomer]


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
