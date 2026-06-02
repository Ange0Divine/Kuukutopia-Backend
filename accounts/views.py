from rest_framework import viewsets, status
from rest_framework.response import Response
from accounts.models import User, StockManager, Customer
from accounts.serializers import UserSerializer, StockManagerSerializer, CustomerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StockManagerViewSet(viewsets.ModelViewSet):
    queryset = StockManager.objects.all()
    serializer_class = StockManagerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
