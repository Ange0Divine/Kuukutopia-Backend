from rest_framework.routers import DefaultRouter
from django.urls import path, include
from inventory.views import ProductsViewSet, BranchViewSet, InventoryViewSet

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'inventory', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]
