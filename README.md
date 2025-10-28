عالی! بر اساس اطلاعاتی که از پروژه دادی (ساختار اپ‌ها، تنظیمات، WebSocket، JWT Middleware، کانفیگ Celery، کانفیگ دیتابیس، و REST API ها)، می‌تونیم یک README جامع و مرتب بسازیم. من یک نسخه پیشنهادی آماده کردم:

---

# Ariana Project

A Django-based project for knowledge management with real-time features using Channels, Celery, and REST APIs.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Project](#running-the-project)
6. [User Roles](#user-roles)
7. [API Endpoints](#api-endpoints)
8. [WebSocket Usage](#websocket-usage)
9. [Celery Tasks](#celery-tasks)
10. [Notes](#notes)

---

## Project Overview

Ariana is a knowledge management system built with Django 5.2.7. It includes:

* REST API for `accounts` and `content` (articles & groups).
* Real-time online users tracking via WebSockets and Channels.
* JWT authentication for APIs and WebSockets.
* Background tasks with Celery (e.g., summary generation).
* Admin interface for managing users, articles, and groups.

---

## Features

* User registration, login, and JWT authentication.
* Password change, refresh, and verification APIs.
* CRUD operations for `Article` and `Group`.
* Online user tracking with WebSockets.
* Celery tasks for async operations like summary generation.
* Role-based permissions via custom permission classes.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mahdiashtian/ariana-project.git
cd ariana-project
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Collect static files:

```bash
python manage.py collectstatic
```

---

## Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

SMS_FROM=+989123456789
SMS_USERNAME=sms_username
SMS_PASSWORD=sms_password

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True

CHANNEL_HOST=localhost
CHANNEL_PORT=6379

BROKER_PROTOCOL=redis
BROKER_HOST=localhost
BROKER_PORT=6379

OPENAI_API_KEY=your-openai-api-key
```

---

## Running the Project

1. Run Django development server:

```bash
python manage.py runserver
```

2. Run Celery worker:

```bash
celery -A core.celery worker -l info
```

## User Roles

* **Admin:** Full access to all models and APIs.
* **Editor:** Can create/update content (articles & groups).
* **Viewer:** Read-only access to content.

---

## API Endpoints

### Accounts

* `/api/auth/login/` – JWT login
* `/api/auth/refresh/` – Refresh token
* `/api/auth/verify/` – Verify token
* `/api/change-password/` – Change password
* `/api/me/` – Get current user info

### Content

* `/api/articles/` – CRUD for articles
* `/api/groups/` – CRUD for groups

All APIs require JWT authentication unless otherwise noted.

---

## WebSocket Usage

* Endpoint: `ws://127.0.0.1:8000/ws/online/`
* Authenticated using JWT in header or query string:

```js
const ws = new WebSocket('ws://127.0.0.1:8000/ws/online/?token=YOUR_JWT_TOKEN');
```

* Middleware `JWTAuthMiddleware` handles authentication.
* Tracks online users in real-time.

---

## Celery Tasks

* `generate_summary_task` – Generates summaries asynchronously for `Knowledge` objects.
* Celery uses Redis as broker (`BROKER_HOST` & `BROKER_PORT` in `.env`).

---

## Notes

* Static files are served from `static_cdn/static_root`.
* Media files are served from `static_cdn/media_root`.
* Channels Redis backend is used for WebSocket communication.
* Custom permission classes are in `library/permissions.py`.
* JWT token expiration: 1 day for access, 10 days for refresh.

---

اگر بخوای می‌تونم همین حالا نسخه فارسیش هم آماده کنم که کاملاً برای داکیومنت داخلی مناسب باشه و شامل توضیحات WebSocket، Celery و نکات پیاده‌سازی پروژه باشه.

میخوای نسخه فارسیش هم بسازم؟
