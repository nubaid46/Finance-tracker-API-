# Finance Tracker API (Django + DRF)

A minimal Finance Tracker REST API built with Django and Django REST Framework.
Provides: user registration, JWT auth, transactions CRUD, saving goals, analytics endpoints, and simple anomaly detection.

## Features
- JWT authentication (access + refresh)
- Transactions (CRUD) per user
- Saving goals with progress percentage
- Analytics endpoint (total spent, category-wise totals, goals)
- Anomaly detection endpoint (rule-based threshold)

## Quick start (local)
1. Clone repo
2. Create and activate a virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
3.Install dependencies:

pip install -r requirements.txt

4.Run migrations:
  python manage.py migrate
5.Optional) Create superuser:

python manage.py createsuperuser
6.Optional) Load sample data:

python manage.py loaddata sample_fixture.json
7.Start the server:

python manage.py runserver
Authentication

Obtain JWT:
POST /api/token/ with {"username":"<user>", "password":"<pass>"}
Response contains access and refresh.

Use Authorization: Bearer <access_token> header for protected endpoints.

Endpoints

POST /api/register/ — register new user

POST /api/token/ — login, get tokens

GET/POST /api/transactions/ — list and create transactions

GET/PUT/DELETE /api/transactions/<id>/ — transaction detail

GET/POST /api/goals/ — list and create saving goals

GET/PUT/DELETE /api/goals/<id>/ — goal detail

GET /api/analytics/ — totals and category breakdown + goals

GET /api/anomalies/?threshold=5000 — show transactions above threshold

Example curl
# Register
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass"}'

# Get tokens
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass"}'

# Use token to create transaction (replace ACCESS)
curl -X POST http://127.0.0.1:8000/api/transactions/ \
  -H "Authorization: Bearer ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"amount":"250.00","category":"Food","description":"Dinner"}'

Notes

This project uses SQLite for local development for convenience. For production, update DATABASES in finance_tracker/settings.py.

SIMPLE_JWT settings are in settings.py.

Anomaly detection is currently rule-based; you can expand it with statistical or ML methods later.

