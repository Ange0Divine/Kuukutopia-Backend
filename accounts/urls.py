from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounts.views import (
    UserViewSet, StockManagerViewSet, CustomerViewSet,
    RegisterView, LoginView, LogoutView,
    FarmerRegisterView, CustomerRegisterView, StockManagerRegisterView,
    ForgotPasswordView, VerifyTokenView, ResetPasswordView, ChangePasswordView,
    UpdateProfileView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'stock-managers', StockManagerViewSet, basename='stockmanager')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/farmer/', FarmerRegisterView.as_view(), name='farmer-register'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer-register'),
    path('register/stock-manager/', StockManagerRegisterView.as_view(), name='stockmanager-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
]
