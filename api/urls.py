from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, UserView, dashboard_view,
    HydroponicSystemViewSet, MeasurementViewSet,
    system_detail_view, add_system, add_sensor, delete_system
)

# Router dla API
router = DefaultRouter()
router.register(r'hydroponic-systems', HydroponicSystemViewSet, basename='hydroponic-system')
router.register(r'measurements', MeasurementViewSet, basename='measurement')

# URL patterns
urlpatterns = [
    # Autoryzacja i użytkownicy
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),

    # API dla systemów hydroponicznych
    path('', include(router.urls)),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("system/<int:system_id>/", system_detail_view, name="system_detail"), 
    path("system/add/", add_system, name="add_system"),  
    path('system/<int:system_id>/add-sensor/', add_sensor, name='add_sensor'),  
    path('system/<int:system_id>/delete/', delete_system, name='delete_system'),
]
