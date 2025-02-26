from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import HydroponicSystem, Measurement

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Konfiguracja widoku użytkowników w panelu admina."""
    list_display = ("id", "username", "email", "is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
    ordering = ("date_joined",)
    list_filter = ("is_staff", "is_active")


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    """Panel administracyjny systemów hydroponicznych."""
    list_display = ("id", "name", "owner", "location", "created_at")
    search_fields = ("name", "owner__username")
    list_filter = ("owner",)  # Możliwość filtrowania po właścicielu


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    """Panel administracyjny pomiarów systemów hydroponicznych."""
    list_display = ("id", "hydroponic_system", "timestamp", "ph", "temperature", "tds")
    search_fields = ("hydroponic_system__name",)
    list_filter = ("hydroponic_system",)  # Możliwość filtrowania po systemie
