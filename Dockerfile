# Wybór oficjalnego obrazu Pythona 3.10
FROM python:3.10

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Skopiowanie plików projektu do kontenera
COPY . /app/

# Instalacja zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Otwarcie portu 8000 dla Django
EXPOSE 8000

# Komenda do uruchomienia aplikacji Django
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 hydroponic.wsgi:application"]