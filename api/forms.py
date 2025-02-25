from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importujemy nasz model użytkownika

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Ustawiamy nasz model
        fields = ("username", "email", "password1", "password2")  # Pola, które chcemy w formularzu
