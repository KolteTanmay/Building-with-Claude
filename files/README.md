# Crafteon Labs — Backend API

FastAPI + PostgreSQL backend for the Crafteon Labs 3D printing website.

---

## Features
- Order form submissions with email + WhatsApp notifications
- Admin dashboard API (JWT protected)
- Gallery item management (CRUD)
- Order status tracking with customer email updates

---

## Setup

### 1. Clone & install dependencies
```bash
cd crafteon-backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your DB URL, SMTP credentials, Twilio keys etc.
```

### 3. Start PostgreSQL and create the database
```sql
CREATE DATABASE crafteon_db;
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

API runs at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs  
Redoc: http://localhost:8000/redoc

---

## API Overview

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/orders/` | Public | Submit a new order |
| GET | `/orders/{id}` | Public | Check order status |
| GET | `/gallery/` | Public | Get all gallery items |
| POST | `/gallery/` | Admin | Add gallery item |
| PUT | `/gallery/{id}` | Admin | Update gallery item |
| DELETE | `/gallery/{id}` | Admin | Delete gallery item |
| POST | `/admin/login` | — | Get JWT token |
| GET | `/admin/orders` | Admin | List all orders |
| GET | `/admin/orders/stats` | Admin | Dashboard stats |
| PATCH | `/admin/orders/{id}` | Admin | Update order status |
| DELETE | `/admin/orders/{id}` | Admin | Delete order |

---

## Notifications
- **Email** — Uses SMTP (works with Gmail App Passwords)
- **WhatsApp** — Uses Twilio API (optional, can leave unconfigured)
- Both fail silently in dev if credentials aren't set

---

## Deployment
Recommended: **Railway** or **Render** (free tiers available)
- Set all `.env` variables in the platform's environment settings
- Use a managed PostgreSQL instance (Railway provides one free)
