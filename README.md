
# Hydroponic System Management

This application is designed for managing hydroponic systems, allowing users to monitor and control environmental parameters such as pH, temperature, and TDS (Total Dissolved Solids) within hydroponic systems.

## Overview
This project enables:

- Managing hydroponic systems via an admin panel.
- Registering and editing hydroponic systems.
- Monitoring parameters such as pH, temperature, and TDS through a built-in API.
- User registration and management by administrators.
- Collecting and processing environmental data.
- Running the application locally or in Docker.

## Features

### Admin Panel
The admin panel allows administrators to:

- **Manage Hydroponic Systems**: Add, edit, or delete hydroponic systems.
- **User Management**: View and edit user data, delete user accounts.
- **Data Monitoring**: Monitor and view system parameters such as pH, temperature, and TDS.

### Users
Registered users can:

- **Log in**: Access their personal accounts.
- **Manage Hydroponic Systems**: View and manage their own hydroponic systems and their parameters.
- **Observe Data**: Monitor environmental data for their systems.
  
Superusers have full access to the application, including managing both users and hydroponic systems.

## Requirements
To run this project, you will need:

- Docker (optional, for containerized deployment)
- Python 3.10+
- PostgreSQL (for storing user and system data)
- Django 5.x
- Django REST Framework (for API handling)
- Pip (for package management)

## Installation

### 1. Local Installation
To install the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/YourRepo/hydroponic-system.git
   cd hydroponic-system
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure PostgreSQL: Ensure you have a working PostgreSQL database. Configure the connection in the `settings.py` file under the `DATABASES` section. The database host is dynamically set based on the environment (localhost for local deployment, `db` for Docker deployment).

4. Run migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser account for accessing the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

   You will be prompted to enter:
   - Username
   - Email address
   - Password

6. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application: Open your browser and navigate to [http://127.0.0.1:8000/accounts/register](http://127.0.0.1:8000/accounts/register).

### 2. Docker Installation
To run the application in Docker:

1. Build the Docker images:

   ```bash
   docker-compose build
   ```

2. Start the containers (both the application and database):

   ```bash
   docker-compose up
   ```

3. Access the application: Open your browser and go to [http://127.0.0.1:8000/accounts/register](http://127.0.0.1:8000/accounts/register) to access the app running in Docker.

## Usage

### Registration and Login

- **User Registration**: Register by providing an email address and password. Once registered, you can log in to your account.
  
- **Admin Login**: Log in to the admin panel using the superuser credentials at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

### Admin Panel
After logging in as an admin, you can:

- **Manage Hydroponic Systems**: Add new systems, edit existing ones, or delete systems.
- **Manage Users**: View and edit user accounts, delete users if necessary.
- **View Data**: Monitor system parameters such as pH, temperature, and TDS.

### User Panel
Registered users can:

- **View Hydroponic Systems**: Display available systems, their parameters, and current status.

## Known Issues and Future Improvements

### Known Issues:
- **Admin Panel Display Issues in Docker**: When running the application in Docker, the admin panel is functional but does not display correctly.

### Planned Improvements:
- **Refactor views.py for SOLID Principles**: The `views.py` file will be refactored to adhere to the SOLID design principles for better maintainability and readability.
- **Unit Tests**: Adding unit tests to improve code coverage and ensure better reliability.
  
