
# Hydroponic System Management

Aplikacja służy do zarządzania systemami hydroponicznymi, umożliwiając monitorowanie i kontrolowanie parametrów środowiskowych takich jak pH, temperatura, i TDS (total dissolved solids) w systemach hydroponicznych.

## Opis

Projekt pozwala na:
- Zarządzanie systemami hydroponicznymi w panelu administracyjnym.
- Rejestrowanie nowych systemów hydroponicznych oraz ich edytowanie.
- Monitorowanie parametrów takich jak pH, temperatura, i TDS za pomocą wbudowanego API.
- Możliwość rejestracji użytkowników oraz zarządzania nimi przez administratora.
- Zbieranie i przetwarzanie danych na temat warunków środowiskowych.
- Uruchamianie aplikacji zarówno lokalnie, jak i w Dockerze.

## Funkcjonalności

### Panel Administratora
W panelu administracyjnym można:
- **Zarządzać systemami hydroponicznymi**: Administrator może dodawać nowe systemy, edytować istniejące lub usuwać je.
- **Zarządzać użytkownikami**: Administrator ma dostęp do pełnej listy użytkowników, może edytować ich dane oraz usuwać konta.
- **Przegląd danych**: Monitorowanie i przegląd parametrów takich jak pH, temperatura i TDS.
  
### Użytkownicy
- **Zarejestrowani użytkownicy** mogą logować się, zarządzać swoimi systemami hydroponicznymi oraz obserwować dane.
- **Superużytkownicy** mają pełny dostęp do aplikacji, w tym do zarządzania użytkownikami i systemami hydroponicznymi.

## Wymagania

Aby uruchomić projekt, potrzebujesz:
- **Docker** (opcjonalnie do uruchomienia w kontenerach)
- **Python 3.10+**
- **PostgreSQL** – baza danych do przechowywania danych o użytkownikach i systemach
- **Django 5.x**
- **Django REST Framework** – do obsługi API
- **Pip** – do instalacji pakietów

## Instalacja

### 1. Instalacja lokalna

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/TwojeRepozytorium/hydroponic-system.git
   cd hydroponic-system
   ```

2. **Zainstaluj wymagane pakiety:**
   Użyj poniższego polecenia, aby zainstalować wszystkie wymagane zależności.
   ```bash
   pip install -r requirements.txt
   ```

3. **Skonfiguruj bazę danych PostgreSQL:**
   Upewnij się, że masz działającą bazę danych PostgreSQL. Możesz skonfigurować połączenie w pliku `settings.py` w sekcji `DATABASES`. Host bazy danych jest dynamicznie określany: jeśli aplikacja jest uruchamiana lokalnie, będzie to `localhost`, jeśli w Dockerze, używa `db` jako hosta.

4. **Wykonaj migracje:**
   Zaktualizuj bazę danych, wykonując migracje.
   ```bash
   python manage.py migrate
   ```

5. **Utwórz superużytkownika:**
   Aby móc zalogować się do panelu administracyjnego, utwórz konto superużytkownika:
   ```bash
   python manage.py createsuperuser
   ```
   Podczas tworzenia superużytkownika, system poprosi o podanie:
   - Nazwy użytkownika
   - Adresu e-mail
   - Hasła

6. **Uruchom serwer:**
   Uruchom lokalny serwer Django:
   ```bash
   python manage.py runserver
   ```

7. **Dostęp do aplikacji:**
   Otwórz przeglądarkę i przejdź do [http://127.0.0.1:8000](http://127.0.0.1:8000), gdzie będzie dostępna aplikacja.

### 2. Instalacja w Dockerze

1. **Zbuduj obrazy:**
   Zbuduj obrazy Docker:
   ```bash
   docker-compose build
   ```

2. **Uruchom kontenery:**
   Uruchom aplikację i bazę danych w Dockerze:
   ```bash
   docker-compose up
   ```

3. **Dostęp do aplikacji:**
   Otwórz przeglądarkę i wejdź na [http://127.0.0.1:8000](http://127.0.0.1:8000), gdzie będzie dostępna aplikacja w kontenerze Docker.

## Użycie aplikacji

### Rejestracja i logowanie

1. **Rejestracja użytkownika:**
   - Zarejestruj się w aplikacji, podając adres e-mail oraz hasło.
   - Po udanej rejestracji możesz zalogować się na swoje konto.

2. **Logowanie do panelu admina:**
   - Zaloguj się do panelu admina, używając utworzonego konta superużytkownika:
   - Adres URL: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

### Panel Administratora

Po zalogowaniu jako admin, będziesz miał dostęp do następujących opcji:

1. **Zarządzanie systemami hydroponicznymi**: Dodawanie nowych systemów, edytowanie istniejących, usuwanie systemów.
2. **Zarządzanie użytkownikami**: Przegląd użytkowników, edytowanie ich danych oraz usuwanie kont.
3. **Przegląd danych**: Przegląd danych dotyczących systemów hydroponicznych (np. pH, temperatura, TDS).

### Panel Użytkownika

Zalogowani użytkownicy mogą:
- **Przeglądać systemy hydroponiczne**: Wyświetlanie dostępnych systemów, ich parametrów i stanu.



