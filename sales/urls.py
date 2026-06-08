from rest_framework.routers import DefaultRouter
from django.urls import path, include
from sales.views import OrderViewSet, PurchaseOrderViewSet, DistributionViewSet, SalesViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-order')
router.register(r'distributions', DistributionViewSet, basename='distribution')
router.register(r'sales', SalesViewSet, basename='sales')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', include(router.urls)),
]
