from django.urls import path, include
from .views import RegisterView, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, MeasurementViewSet
from .views import register_view, dashboard_view
from .views import system_detail_view
from .views import add_system

# Rejestracja routera dla HydroponicSystemViewSet
router = DefaultRouter()
router.register(r'hydroponic-systems', HydroponicSystemViewSet, basename='hydroponic-system')
router.register(r'measurements', MeasurementViewSet, basename='measurement')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('', include(router.urls)),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("system/<int:system_id>/", system_detail_view, name="system_detail"), 
    path("add-system/", add_system, name="add_system"),
]