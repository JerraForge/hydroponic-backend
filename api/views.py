from rest_framework import generics, viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.http import JsonResponse
import random
from django.utils.timezone import now

from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from .forms import CustomUserCreationForm

User = get_user_model()

# ✅ Rejestracja użytkownika
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


# ✅ Logowanie JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


# ✅ Pobieranie danych użytkownika
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        })


# ✅ CRUD dla systemów hydroponicznych
class HydroponicSystemViewSet(viewsets.ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ✅ Widok rejestracji w przeglądarce
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


# ✅ Widok dashboardu użytkownika
@login_required
def dashboard_view(request):
    user_systems = HydroponicSystem.objects.filter(owner=request.user)
    return render(request, "dashboard.html", {"systems": user_systems})


# ✅ API dla pomiarów hydroponicznych
class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']

    def get_queryset(self):
        return Measurement.objects.filter(hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        hydroponic_system = serializer.validated_data["hydroponic_system"]
        if hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError("Nie masz uprawnień do tego systemu.")
        serializer.save()


# ✅ Szczegóły systemu + filtrowanie i paginacja
@login_required
def system_detail_view(request, system_id):
    system = get_object_or_404(HydroponicSystem, id=system_id)

    # Pobieranie wszystkich pomiarów dla systemu
    measurements = Measurement.objects.filter(hydroponic_system=system).order_by('-timestamp')

    # **✅ FILTROWANIE PO Dacie**
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

    # **✅ FILTROWANIE PO TYPACH POMIARÓW (pH, temperatura, TDS)**
    show_ph = request.GET.get('show_ph') == 'on'
    show_temperature = request.GET.get('show_temperature') == 'on'
    show_tds = request.GET.get('show_tds') == 'on'

    # Jeśli użytkownik nic nie wybrał → pokaż wszystko
    if not (show_ph or show_temperature or show_tds):
        show_ph = show_temperature = show_tds = True

    # **✅ FILTROWANIE PO WARTOŚCIACH**
    filter_type = request.GET.get('filter_type', '')
    min_value = request.GET.get('min_value')
    max_value = request.GET.get('max_value')

    if min_value:
        try:
            min_value = float(min_value)
            if filter_type == 'ph':
                measurements = measurements.filter(ph__gte=min_value)
            elif filter_type == 'temperature':
                measurements = measurements.filter(temperature__gte=min_value)
            elif filter_type == 'tds':
                measurements = measurements.filter(tds__gte=min_value)
        except ValueError:
            pass  # Ignoruj błędy konwersji

    if max_value:
        try:
            max_value = float(max_value)
            if filter_type == 'ph':
                measurements = measurements.filter(ph__lte=max_value)
            elif filter_type == 'temperature':
                measurements = measurements.filter(temperature__lte=max_value)
            elif filter_type == 'tds':
                measurements = measurements.filter(tds__lte=max_value)
        except ValueError:
            pass  # Ignoruj błędy konwersji

    # **✅ PAGINACJA**
    paginator = Paginator(measurements, 10)  # 10 wyników na stronę
    page = request.GET.get('page')
    measurements = paginator.get_page(page)

    context = {
        'system': system,
        'measurements': measurements,
        'filter_type': filter_type,
        'min_value': min_value,
        'max_value': max_value,
        'show_ph': show_ph,
        'show_temperature': show_temperature,
        'show_tds': show_tds,
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'paginator': paginator
    }
    return render(request, 'system_detail.html', context)


# ✅ Dodawanie nowego systemu hydroponicznego
@login_required
def add_system(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location", "")
        if name:
            HydroponicSystem.objects.create(name=name, location=location, owner=request.user)
    return redirect("dashboard")


# ✅ Symulowany czujnik – automatyczne pomiary
@login_required
def add_sensor(request, system_id):
    system = get_object_or_404(HydroponicSystem, id=system_id, owner=request.user)

    for _ in range(5):  # 5 pomiarów co 2 minuty (przykładowo)
        Measurement.objects.create(
            hydroponic_system=system,
            ph=round(random.uniform(5.5, 8.5), 2),
            temperature=round(random.uniform(18, 26), 2),
            tds=random.randint(300, 1500),
            timestamp=now()
        )

    return JsonResponse({"message": "Czujnik dodany, wygenerowano pomiary!"})


# ✅ Usuwanie systemu hydroponicznego
@login_required
def delete_system(request, system_id):
    system = get_object_or_404(HydroponicSystem, id=system_id, owner=request.user)
    system.delete()
    return redirect("dashboard")
