# Workout Logger API

A REST API for the Workout Logger application, built with Django and Django REST Framework.

## Tech Stack

- **Python 3.12+**
- **Django 6** — web framework
- **Django REST Framework** — API layer
- **django-cors-headers** — cross-origin request handling
- **PostgreSQL** — database (production via Railway)
- **SQLite** — database fallback (local dev, no `DATABASE_URL` set)
- **dj-database-url** — parses the `DATABASE_URL` environment variable
- **Token Authentication** — DRF token auth

## Project Structure

```
workout_logger_api/
├── fixtures/          # Seed data (users, exercises, logs, etc.)
├── migrations/        # Database migrations
├── models/
│   ├── exercise.py         # Category, MuscleGroup, Exercise, MuscleExercise
│   ├── intensity.py        # Intensity
│   ├── workout_log.py      # WorkoutLog
│   ├── log_exercise.py     # LogExercise (join: log ↔ exercise)
│   ├── workout_log_like.py # WorkoutLogLike
│   └── workout_log_comment.py # WorkoutLogComment
└── views/
    ├── auth.py             # Register, Login, Logout
    ├── categories.py       # Category list
    ├── exercises.py        # Exercise list + create + edit/delete (owner only)
    ├── muscle_groups.py    # Muscle group list
    ├── intensity.py        # Intensity list
    ├── workout_logs.py     # Log CRUD + community feed
    ├── likes.py            # Like / unlike toggle
    └── comments.py         # Comment create + delete
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Production only | Full Postgres connection string. Railway injects this automatically when you add a PostgreSQL plugin. If absent, the app falls back to a local SQLite file. |
| `SECRET_KEY` | Production | Django secret key. Set this to a long random string in Railway; never commit the production value. |
| `ALLOWED_HOSTS` | Production | Comma-separated list of allowed hostnames (e.g. your Railway domain). |

## Setup

### 1. Install dependencies

```bash
poetry install
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Seed the database

```bash
bash seed_database.sh
```

This flushes the database and loads all fixture data. See the **Fixtures** section below for details.

> **Warning:** `seed_database.sh` runs `flush` first, which wipes all existing data.

### 4. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

## Fixtures

Fixture files live in `workout_logger_api/fixtures/`. The seed script loads them in dependency order:

| Fixture | Contents |
|---|---|
| `users.json` | 4 test accounts (all share the same password) |
| `tokens.json` | Auth tokens for each user |
| `intensity.json` | Intensity levels (Light, Moderate, Hard, Max) |
| `muscle_groups.json` | Muscle group reference data |
| `categories.json` | Workout categories (Push, Pull, Legs, Core, Cardio) |
| `exercises.json` | 10 seed exercises, each assigned to a user via `created_by` |
| `muscle_exercises.json` | Exercise ↔ muscle group associations |
| `workout_logs.json` | Sample workout logs |
| `log_exercises.json` | Exercises within each log |

**Test credentials** (all accounts use the same password):

| Username | Password |
|---|---|
| `testuser` | `testpassword123` |
| `jsmith` | `testpassword123` |
| `ajohnson` | `testpassword123` |
| `mwilliams` | `testpassword123` |

## API Endpoints

All endpoints are prefixed with `/api/`.

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register/` | Create a new account |
| POST | `/auth/login/` | Obtain an auth token |
| POST | `/auth/logout/` | Revoke the auth token |

### Reference Data

| Method | Endpoint | Description |
|---|---|---|
| GET | `/categories/` | List all workout categories |
| GET | `/intensity/` | List all intensity levels |
| GET | `/muscle-groups/` | List all muscle groups |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises/` | List all exercises |
| POST | `/exercises/` | Create an exercise (sets `created_by` to requesting user) |
| PUT | `/exercises/<id>/` | Edit an exercise (owner only) |
| DELETE | `/exercises/<id>/` | Delete an exercise (owner only) |

### Workout Logs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/logs/` | List the authenticated user's logs |
| POST | `/logs/` | Create a new log |
| GET | `/logs/<id>/` | Retrieve a single log |
| PUT | `/logs/<id>/` | Update a log |
| DELETE | `/logs/<id>/` | Delete a log |
| GET | `/logs/community/` | List all users' logs (includes likes + comments) |

### Likes & Comments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/logs/<id>/like/` | Toggle like on a community log |
| POST | `/logs/<id>/comments/` | Post a comment on a log |
| DELETE | `/logs/<id>/comments/<comment_id>/` | Delete your own comment |

## Authentication

All endpoints require a valid token. Include it in the `Authorization` header:

```
Authorization: Token <your-token>
```
