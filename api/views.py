from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import HydroponicSystem
from .serializers import HydroponicSystemSerializer

User = get_user_model()

# Serializer do rejestracji użytkowników
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Widok rejestracji użytkownika
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })    

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    API do zarządzania systemami hydroponicznymi (CRUD).
    """
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]  # Tylko zalogowani użytkownicy

    def get_queryset(self):
        """Zwraca tylko systemy hydroponiczne należące do zalogowanego użytkownika"""
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Przypisuje właściciela systemu hydroponicznego do zalogowanego użytkownika"""
        serializer.save(owner=self.request.user)