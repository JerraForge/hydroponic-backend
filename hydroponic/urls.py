from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from api.views import register_view, dashboard_view  # Importujemy tylko te widoki, które są faktycznie używane

urlpatterns = [
    # Panel administratora
    path('admin/', admin.site.urls),

    # API (wszystkie endpointy REST)
    path('api/', include('api.urls')),

    # System uwierzytelniania
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),  # Przekierowanie po wylogowaniu
    path("accounts/register/", register_view, name="register"),

    # Dashboard użytkownika
    path("dashboard/", dashboard_view, name="dashboard"),
]
