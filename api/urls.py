from django.urls import path, include
from .views import RegisterView, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet

router = DefaultRouter()
router.register(r'hydroponic-systems', HydroponicSystemViewSet, basename='hydroponic-system')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('', include(router.urls)),
]
