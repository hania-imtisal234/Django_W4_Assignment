# Hospital Management System

This Django-based Hopital Management System is designed to manage doctors, patients, appointments, and medical records. The application includes functionality for patients, doctors, and administrators, each with their specific access and permissions.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Virtual Environment](#virtual-environment)
  - [Install Requirements](#install-requirements)
- [Usage](#usage)
  - [Starting the Server](#starting-the-server)
  - [Admin Access](#admin-access)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- User roles: Patient, Doctor, and Admin
- Secure authentication and permission handling
- Manage and view appointments
- Add, edit, and view medical records
- Custom error pages

## Prerequisites

- Python 3.10+
- Django 5.1+
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Setup

### Virtual Environment

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
2. **Activate the virtual environment:**
    - On Windows:
      ```bash
      .\venv\Scripts\activate
    - On macOS/Linux:
       ```bash
       source venv/bin/activate
### Install Requirements
- Once the virtual environment is activated, install the required packages:

  ```bash
  pip install -r requirements.txt
- **Database**
- Before running the project, you need to apply the migrations:
  ```bash
  python manage.py migrate
- **Create a Superuser**
- To access the admin interface, you need to create a superuser:
  ```bash
  python manage.py createsuperuser
## Usage
### Starting the Server
  - To start the Django development server, run:
     ```bash
     python manage.py runserver
  - Access the application at http://127.0.0.1:8000/.

### Admin Access
  - The admin panel can be accessed at http://127.0.0.1:8000/admin/.

### Project Structure:
   - config/: Contains the main project settings and URL 
     configurations.
   - web/: The core application that includes:
   - appointments/: Manages appointments between doctors and 
     patients.
   - medical_records/: Manages medical records for patients.
   - users/: Handles user management including authentication and 
     permissions with user management for admin.
   - templates/: Contains HTML templates for the application.
   - static/: Stores static files like CSS, JavaScript, and images.
   - media/: Stores uploaded files like medical reports.
