from rest_framework.routers import DefaultRouter
from django.urls import path, include
from sales.views import OrderViewSet, SalesViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'sales', SalesViewSet, basename='sales')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', include(router.urls)),
]
