from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounts.views import UserViewSet, StockManagerViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'stock-managers', StockManagerViewSet, basename='stockmanager')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
