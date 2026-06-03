from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from accounts.models import User, StockManager, Customer
from accounts.serializers import UserSerializer, StockManagerSerializer, CustomerSerializer, FarmerRegisterSerializer, CustomerRegisterSerializer


class RegisterView(APIView):
    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @extend_schema(
        request={'application/json': {'type': 'object', 'properties': {'username': {'type': 'string'}, 'password': {'type': 'string'}}}},
        responses={'200': {'type': 'object', 'properties': {'token': {'type': 'string'}}}}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class LogoutView(APIView):
    @extend_schema(request=None, responses={'200': {'type': 'object', 'properties': {'message': {'type': 'string'}}}})
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class FarmerRegisterView(APIView):
    @extend_schema(request=FarmerRegisterSerializer, responses=FarmerRegisterSerializer)
    def post(self, request):
        serializer = FarmerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class CustomerRegisterView(APIView):
    @extend_schema(request=CustomerRegisterSerializer, responses=CustomerRegisterSerializer)
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StockManagerViewSet(viewsets.ModelViewSet):
    queryset = StockManager.objects.all()
    serializer_class = StockManagerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
