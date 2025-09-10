# Zeno AI - Economic Agent

## Overview

Zeno AI is an advanced AI-powered economic reasoning system designed to provide intelligent insights and predictions to support economic decision-making. The project features a Django REST Framework backend API with endpoints for user management, reviews, conversations, agents, tools, and runs. Interactive API documentation is provided via Swagger and Redoc.

## Features

- User registration, login, and authentication
- CRUD operations on users, reviews, conversations, agents, tools, steps, and runs
- API documentation with Swagger UI and Redoc
- Modular architecture for easy extension and maintenance
- Secure endpoints with configurable authentication and permissions

## Technology Stack

- Python 3.13+
- Django 4.2+
- Django REST Framework
- drf-yasg (Swagger / Redoc API docs)
- PostgreSQL
- Token authentication

## Getting Started

### Prerequisites

- Python 3.13 or higher
- pip package manager
- Virtual environment tool
- Database

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/akirachix/zeno-backend.git
   cd zeno-ai
   ```

2. Create and activate a virtual environment:

   **Linux/macOS:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   **Windows:**

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

4. Set environment variables and update `settings.py`

   - Configure your database, secret keys, and static/media paths

5. Run database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

## API Documentation

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Usage

- Access API root at [http://localhost:8000/](http://localhost:8000/) to explore available endpoints.
- Use `/register/`, `/login/`, and other API endpoints for user authentication and resource management.
- Modify authentication and permission settings in `settings.py` according to your needs.