# Standardowe importy
import random
from datetime import datetime

# Importy Django
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.utils.timezone import now

# Importy Django REST Framework
from rest_framework import generics, viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

# Importy DRF Simple JWT
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Lokalne importy
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from .forms import CustomUserCreationForm

# Pobranie modelu użytkownika
User = get_user_model()


class RegisterSerializer(ModelSerializer):
    """
    Serializer do rejestracji użytkownika.
    Obsługuje tworzenie nowych użytkowników.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Tworzy i zwraca nową instancję użytkownika.
        """
        return User.objects.create_user(**validated_data)


class RegisterView(generics.CreateAPIView):
    """
    Widok API do rejestracji użytkownika.
    Pozwala na rejestrację każdemu użytkownikowi (uwierzytelnionemu lub nie).
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Niestandardowy widok do uzyskiwania tokenów JWT.
    Wykorzystuje domyślny TokenObtainPairSerializer.
    """

    serializer_class = TokenObtainPairSerializer


class UserView(APIView):
    """
    Widok API do pobierania danych uwierzytelnionego użytkownika.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Zwraca dane uwierzytelnionego użytkownika.
        """
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        })


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    ViewSet do operacji CRUD na modelach HydroponicSystem.
    Zezwala tylko na dostęp do systemów należących do uwierzytelnionego użytkownika.
    """

    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Zwraca queryset instancji HydroponicSystem należących do uwierzytelnionego użytkownika.
        """
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Przypisuje utworzony system hydroponiczny do uwierzytelnionego użytkownika.
        """
        serializer.save(owner=self.request.user)


def register_view(request):
    """
    Widok do rejestracji użytkownika przez przeglądarkę.
    Obsługuje przesyłanie formularza i logowanie użytkownika po udanej rejestracji.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard_view(request):
    """
    Widok panelu użytkownika.
    Wyświetla listę systemów hydroponicznych należących do uwierzytelnionego użytkownika.
    """
    user_systems = HydroponicSystem.objects.filter(owner=request.user)
    return render(request, "dashboard.html", {"systems": user_systems})


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    ViewSet do operacji CRUD na modelach Measurement.
    Zezwala tylko na dostęp do pomiarów powiązanych z systemami należącymi do uwierzytelnionego użytkownika.
    Obsługuje sortowanie według znacznika czasu.
    """

    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']

    def get_queryset(self):
        """
        Zwraca queryset instancji Measurement powiązanych z systemami należącymi do uwierzytelnionego użytkownika.
        """
        return Measurement.objects.filter(hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        """
        Sprawdza, czy uwierzytelniony użytkownik jest właścicielem systemu, zanim zapisze pomiar.
        """
        hydroponic_system = serializer.validated_data["hydroponic_system"]
        if hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError("Nie masz uprawnień do dodawania pomiarów do tego systemu.")
        serializer.save()


@login_required
def system_detail_view(request, system_id):
    """
    Widok szczegółów systemu hydroponicznego.
    Obsługuje filtrowanie, paginację i zoptymalizowane zapytania do bazy danych.
    """
    system = get_object_or_404(HydroponicSystem.objects.prefetch_related("measurements"), id=system_id)

    # Pobieranie pomiarów dla systemu z optymalizacją zapytań
    measurements = Measurement.objects.filter(hydroponic_system=system).select_related("hydroponic_system__owner").order_by('-timestamp')

    # Filtrowanie po dacie
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            measurements = measurements.filter(timestamp__date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            measurements = measurements.filter(timestamp__date__lte=end_date)

    # Filtrowanie po typie pomiaru
    show_ph = request.GET.get('show_ph') == 'on'
    show_temperature = request.GET.get('show_temperature') == 'on'
    show_tds = request.GET.get('show_tds') == 'on'

    if not (show_ph or show_temperature or show_tds):
        show_ph = show_temperature = show_tds = True

    # Filtrowanie po wartościach
    filter_type = request.GET.get('filter_type', '')
    min_value = request.GET.get('min_value')
    max_value = request.GET.get('max_value')

    try:
        min_value = float(min_value) if min_value else None
        max_value = float(max_value) if max_value else None

        if filter_type == 'ph':
            if min_value: measurements = measurements.filter(ph__gte=min_value)
            if max_value: measurements = measurements.filter(ph__lte=max_value)
        elif filter_type == 'temperature':
            if min_value: measurements = measurements.filter(temperature__gte=min_value)
            if max_value: measurements = measurements.filter(temperature__lte=max_value)
        elif filter_type == 'tds':
            if min_value: measurements = measurements.filter(tds__gte=min_value)
            if max_value: measurements = measurements.filter(tds__lte=max_value)
    except ValueError:
        pass  # Ignorowanie błędów konwersji

    # Paginacja
    paginator = Paginator(measurements, 10)
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except ValueError:
        page = 1  # Domyślnie pierwsza strona, jeśli podano nieprawidłowy numer strony

    measurements = paginator.get_page(page)

    # Kontekst dla szablonu
    context = {
        'system': system,
        'measurements': measurements,
        'start_date': start_date or '',
        'end_date': end_date or '',
        'show_ph': show_ph,
        'show_temperature': show_temperature,
        'show_tds': show_tds,
        'filter_type': filter_type,
        'min_value': min_value or '',
        'max_value': max_value or '',
        'request': request  # Przekazanie requestu do paginacji
    }

    return render(request, 'system_detail.html', context)


@login_required
def add_system(request):
    """
    Widok do dodawania nowego systemu hydroponicznego.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location", "")
        if name:
            HydroponicSystem.objects.create(name=name, location=location, owner=request.user)
    return redirect("dashboard")


@login_required
def add_sensor(request, system_id):
    """
    Symuluje dodanie czujnika i generuje losowe pomiary pH, temperatury i TDS.
    """
    system = get_object_or_404(HydroponicSystem, id=system_id, owner=request.user)

    # Tworzenie nowego pomiaru z losowymi wartościami
    measurement = Measurement.objects.create(
        hydroponic_system=system,
        ph=round(random.uniform(5.5, 8.5), 2),
        temperature=round(random.uniform(18, 26), 2),
        tds=random.randint(300, 1500),
        timestamp=now()
    )

    return JsonResponse({
        "message": "Czujnik dodany, wygenerowano pomiary!",
        "measurement": {
            "timestamp": measurement.timestamp.strftime("%Y-%m-%d %H:%M"),
            "ph": measurement.ph,
            "temperature": measurement.temperature,
            "tds": measurement.tds
        }
    })


@login_required
def delete_system(request, system_id):
    """
    Widok do usuwania systemu hydroponicznego.
    """
    system = get_object_or_404(HydroponicSystem, id=system_id, owner=request.user)
    system.delete()
    return redirect("dashboard")