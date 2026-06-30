# Ledgerly

A REST API for personal finance tracking — record income and expenses, organize them by category, and pull spending reports through clean, authenticated endpoints.

Built with Django and Django REST Framework, using JWT for authentication and per-user data isolation enforced at the queryset level.

## Features

- JWT-based authentication (access + refresh tokens)
- Per-user data isolation — every user only ever sees their own transactions and profile
- Full CRUD on transactions (income and expenses)
- User profile with currency preference and monthly income
- Monthly income vs expense summary report
- Category-wise spending breakdown report
- Filtering transactions by category, type, and date range

## Tech stack

- Python / Django
- Django REST Framework
- djangorestframework-simplejwt (JWT authentication)
- django-filter (query param filtering)
- SQLite (development) — swap to PostgreSQL via `DATABASE_URL` for production

## Setup

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/Meghansh-Maurya/ledgerly.git
cd ledgerly
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/`.

## Authentication

All endpoints (except token generation) require a valid JWT access token.

**Get a token:**

```
POST /api/v1/token/
```
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

**Use the token** on every other request:
```
Authorization: Bearer <access_token>
```

Refresh an expired access token:
```
POST /api/v1/token/refresh/
```
```json
{
    "refresh": "<refresh_token>"
}
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/token/` | Obtain access + refresh token |
| POST | `/api/v1/token/refresh/` | Refresh access token |

### Profile
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/users/` | Get current user's profile |
| POST | `/api/v1/users/` | Create profile |
| GET | `/api/v1/users/{id}/` | Retrieve profile |
| PUT | `/api/v1/users/{id}/` | Update profile |
| DELETE | `/api/v1/users/{id}/` | Delete profile |

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/transactions/` | List current user's transactions |
| POST | `/api/v1/transactions/` | Create a transaction |
| GET | `/api/v1/transactions/{id}/` | Retrieve a transaction |
| PUT | `/api/v1/transactions/{id}/` | Update a transaction |
| DELETE | `/api/v1/transactions/{id}/` | Delete a transaction |
| GET | `/api/v1/transactions/reports/summary/` | Current month income, expense, savings |
| GET | `/api/v1/transactions/reports/by_category/` | Current month spending grouped by category |

### Filtering

The transaction list endpoint supports query params:

```
GET /api/v1/transactions/?category=food
GET /api/v1/transactions/?type=expense
GET /api/v1/transactions/?date_after=2026-06-01&date_before=2026-06-30
```

## Sample requests

**Create a transaction:**
```
POST /api/v1/transactions/
```
```json
{
    "name": "Swiggy",
    "type": "expense",
    "category": "food",
    "description": "Dinner",
    "date": "2026-06-29",
    "amount": "200.00"
}
```

**Monthly summary response:**
```json
{
    "income": 50000,
    "expense": 8000,
    "savings": 42000
}
```

**Category breakdown response:**
```json
[
    {"category": "food", "total": 3000},
    {"category": "rent", "total": 150000}
]
```

## Security notes

- `user` field is read-only on all serializers — it's always assigned server-side from the authenticated request, never accepted as input.
- All querysets are filtered by `request.user` — no endpoint returns data belonging to another user.
- JWT access tokens expire after 1 day; refresh tokens after 7 days.
