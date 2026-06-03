from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, StockManager, Customer
from accounts.serializers import UserSerializer, StockManagerSerializer, CustomerSerializer, FarmerRegisterSerializer, CustomerRegisterSerializer, StockManagerRegisterSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request={'application/json': {'type': 'object', 'properties': {'username': {'type': 'string'}, 'password': {'type': 'string'}}}},
        responses={'200': {'type': 'object', 'properties': {'access': {'type': 'string'}, 'refresh': {'type': 'string'}}}}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': UserSerializer(user).data})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={'200': {'type': 'object', 'properties': {'message': {'type': 'string'}}}})
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class FarmerRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=FarmerRegisterSerializer, responses=FarmerRegisterSerializer)
    def post(self, request):
        serializer = FarmerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=CustomerRegisterSerializer, responses=CustomerRegisterSerializer)
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class StockManagerRegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(request=StockManagerRegisterSerializer, responses=StockManagerRegisterSerializer)
    def post(self, request):
        serializer = StockManagerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class StockManagerViewSet(viewsets.ModelViewSet):
    queryset = StockManager.objects.all()
    serializer_class = StockManagerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
