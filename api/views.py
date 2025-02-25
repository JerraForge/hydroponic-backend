from rest_framework import generics, viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import HydroponicSystem
from .serializers import HydroponicSystemSerializer
from .forms import CustomUserCreationForm

from .models import Measurement
from .serializers import MeasurementSerializer
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


User = get_user_model()


class RegisterSerializer(ModelSerializer):
    """
    Serializer do rejestracji nowych użytkowników.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Tworzy nowego użytkownika i zwraca jego instancję."""
        user = User.objects.create_user(**validated_data)
        return user


class RegisterView(generics.CreateAPIView):
    """
    Widok API do rejestracji nowych użytkowników.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Widok API do obsługi tokenów JWT (logowanie).
    """
    serializer_class = TokenObtainPairSerializer


class UserView(APIView):
    """
    API do pobierania danych zalogowanego użytkownika.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Zwraca informacje o aktualnie zalogowanym użytkowniku."""
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    API do zarządzania systemami hydroponicznymi (CRUD).
    Każdy użytkownik może zarządzać tylko swoimi systemami.
    """
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Zwraca tylko systemy hydroponiczne należące do zalogowanego użytkownika."""
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Przypisuje właściciela systemu hydroponicznego do zalogowanego użytkownika."""
        serializer.save(owner=self.request.user)


def register_view(request):
    """
    Widok rejestracji użytkownika w przeglądarce.
    Obsługuje formularz Django do rejestracji.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # Możesz zmienić przekierowanie na inną stronę
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard_view(request):
    """
    Widok panelu użytkownika po zalogowaniu.
    Wyświetla listę systemów hydroponicznych użytkownika.
    """
    user_systems = HydroponicSystem.objects.filter(owner=request.user)
    return render(request, "dashboard.html", {"systems": user_systems})



class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API do zarządzania pomiarami systemów hydroponicznych.
    Pozwala na dodawanie i pobieranie pomiarów.
    """
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']

    def get_queryset(self):
        """
        Zwraca tylko pomiary należące do systemów hydroponicznych użytkownika.
        """
        return Measurement.objects.filter(hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        """
        Zapisuje pomiar tylko do systemów hydroponicznych należących do użytkownika.
        """
        hydroponic_system = serializer.validated_data["hydroponic_system"]
        if hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError("Nie masz uprawnień do tego systemu hydroponicznego.")
        serializer.save()


@login_required
def system_detail_view(request, system_id):
    """
    Wyświetla szczegóły wybranego systemu hydroponicznego.
    """
    system = get_object_or_404(HydroponicSystem, id=system_id, owner=request.user)
    measurements = system.measurements.all().order_by("-timestamp")[:10]  # Pobiera 10 ostatnich pomiarów
    return render(request, "system_detail.html", {"system": system, "measurements": measurements})


@login_required
def add_system(request):
    """
    Widok obsługujący dodawanie nowego systemu hydroponicznego.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location", "")

        if name:  # Sprawdzamy, czy podano nazwę
            HydroponicSystem.objects.create(
                name=name,
                location=location,
                owner=request.user
            )
            messages.success(request, "System hydroponiczny został dodany.")
        else:
            messages.error(request, "Nazwa systemu jest wymagana!")

    return redirect("dashboard")



