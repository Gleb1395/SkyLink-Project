# SkyLink-Project (Study Project)

**SkyLink** - is a REST API for managing the airport model. The project allows you to create and view flights, routes, tickets and orders. The service implements full CRUD for all entities and also includes sending PDF tickets to email and Telegram.
#
### Basic functionality:
+ Full CRUD for flights, routes, airports, airplanes, seats, tickets and bookings
+ Send PDF ticket to email and Telegram
+ Authentication with JWT
+ Documentation via Swagger and drf-spectacular
+ Using standard Django REST Framework features (serializers, managers, view classes, etc.)
+ Sending emails via Gmail SMTP
+ Automated tests and code validation by linters (flake8, isort, black)
+ Docker and Docker Compose
+ Connected services:
  + PostgreSQL
  + Redis
  + Celery + Celery Beat
+ Flower
+ PgAdmin
+ CI/CD process via GitHub Actions

## ER-diagram of the project
![image](https://github.com/user-attachments/assets/ebef636a-fc3a-4144-9ca8-ef14177b5521)

## Installation
``` python
python -m venv venv
venv\Scripts\activate 
pip install -r requirements.txt
docker-compose up --build
```
## Authentication
Authentication is implemented using JWT (SimpleJWT).

## Documentation
Swagger documentation is available at: api/schema/swagger-ui/

## Integration with Telegram
After a successful ticket purchase, a PDF file of the ticket can be sent to the user via Telegram-bot (telebot library is used).

## Email Notifications
The PDF ticket is also sent to the user's email via SMTP (Gmail).

## Periodic tasks
Periodic tasks are set up using Celery Beat.