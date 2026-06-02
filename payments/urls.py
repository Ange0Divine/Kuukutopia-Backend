from rest_framework.routers import DefaultRouter
from django.urls import path, include
from payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
