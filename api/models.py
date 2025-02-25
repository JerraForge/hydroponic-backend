from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Model użytkownika oparty na Django AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email musi być unikalny

    def __str__(self):
        return self.username

# Model systemu hydroponicznego
class HydroponicSystem(models.Model):
    name = models.CharField(max_length=100)  # Nazwa systemu
    location = models.CharField(max_length=255, blank=True, null=True)  # Opcjonalna lokalizacja
    created_at = models.DateTimeField(auto_now_add=True)  # Data utworzenia
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Właściciel systemu

    def __str__(self):
        return self.name

#  Model pomiarów czujników
class Measurement(models.Model):
    hydroponic_system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name='measurements'
    )  # Każdy pomiar należy do konkretnego systemu
    timestamp = models.DateTimeField(auto_now_add=True)  # Czas pomiaru
    ph = models.FloatField()  # Pomiar pH
    temperature = models.FloatField()  # Pomiar temperatury wody
    tds = models.FloatField()  # Pomiar całkowitej ilości rozpuszczonych substancji (TDS)

    def __str__(self):
        return f"{self.hydroponic_system.name} - {self.timestamp}"
