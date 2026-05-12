````md
# Chronos

Chronos is a Distributed Job Scheduling System built using FastAPI, MySQL, SQLAlchemy, APScheduler, and Docker.

The system supports:
- one-time scheduled jobs
- recurring cron jobs
- job management
- retry handling
- monitoring and logging
- JWT authentication
- Dockerized deployment

The initial implemented job type is:
- TELEGRAM_MESSAGE

---

# Features

## Job Submission
- Immediate jobs
- Scheduled jobs
- Generic job types

## Recurring Jobs
- Cron-based recurring jobs

## Job Management
- Create jobs
- View jobs
- Get single job details
- Cancel jobs
- Reschedule jobs

## Failure Handling
- Automatic retries
- Retry tracking
- Failure logging

## Logging & Monitoring
- Execution logs
- Health check API
- Statistics API

## Authentication
- JWT Authentication
- Protected APIs

## Dockerized Deployment
- FastAPI container
- MySQL container
- Persistent database volume

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Scheduler | APScheduler |
| Authentication | JWT |
| Containerization | Docker |
| External Integration | Telegram Bot API |

---

# System Architecture

Chronos uses a modular handler-based architecture.

Each job type has its own handler.

Example:

```python
JOB_HANDLERS = {
    "TELEGRAM_MESSAGE": TelegramHandler()
}
```

This allows future job types to be added without modifying scheduler logic.

Possible future job types:
- EMAIL_NOTIFICATION
- FILE_BACKUP
- WEBHOOK_CALL
- REPORT_GENERATION

---

# Project Structure

```text
app/
├── api/
├── core/
├── db/
├── job_handlers/
├── models/
├── scheduler/
├── schemas/
├── services/
└── main.py
```

---

# Database Tables

## users
Stores registered users.

## jobs
Stores scheduled jobs and metadata.

## job_execution_logs
Stores execution history and failure logs.

---

# Local Setup

## 1. Clone Repository

```bash
git clone <repo-url>
cd chronos
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install MySQL

```bash
sudo apt update
sudo apt install mysql-server -y
```

---

## 5. Create Database

```sql
CREATE DATABASE chronos;
```

---

## 6. Create MySQL User

```sql
CREATE USER 'chronos'@'localhost' IDENTIFIED BY 'chronos123';

GRANT ALL PRIVILEGES ON chronos.* TO 'chronos'@'localhost';

FLUSH PRIVILEGES;
```

---

## 7. Configure Environment Variables

Create `.env`

```env
DATABASE_URL=mysql+pymysql://chronos:chronos123@localhost/chronos

SECRET_KEY=supersecretkey

ALGORITHM=HS256

TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
```

---

# Telegram Bot Setup

## Create Bot

Open Telegram and search:

```text
BotFather
```

Create bot:

```text
/newbot
```

Copy generated token into `.env`

---

## Get Chat ID

Message the bot once.

Open:

```text
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

Copy:

```json
chat.id
```

Example:

```text
5141275856
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# Docker Setup

## Prerequisites

Install:
- Docker
- Docker Compose

Verify:

```bash
docker --version
docker compose version
```

---

# Docker Files

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## docker-compose.yml

```yaml
services:

  mysql:
    image: mysql:8.0
    container_name: chronos-mysql

    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: chronos
      MYSQL_USER: chronos
      MYSQL_PASSWORD: chronos123

    ports:
      - "3307:3306"

    volumes:
      - mysql_data:/var/lib/mysql

  chronos:
    build: .

    container_name: chronos-app

    depends_on:
      - mysql

    ports:
      - "8000:8000"

    environment:
      DATABASE_URL: mysql+pymysql://chronos:chronos123@mysql/chronos
      SECRET_KEY: supersecretkey
      ALGORITHM: HS256
      TELEGRAM_BOT_TOKEN: YOUR_BOT_TOKEN

    volumes:
      - .:/app

    command: >
      sh -c "
      sleep 10 &&
      uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
      "

volumes:
  mysql_data:
```

---

# Run Using Docker

## Build

```bash
docker compose build --no-cache
```

---

## Start Containers

```bash
docker compose up
```

---

## Run In Background

```bash
docker compose up -d
```

---

## Stop Containers

```bash
docker compose down
```

---

# Docker Access

## FastAPI

```text
http://127.0.0.1:8000
```

## Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

# View Logs

## App Logs

```bash
docker logs chronos-app
```

## MySQL Logs

```bash
docker logs chronos-mysql
```

---

# Authentication APIs

## Register

POST `/auth/register`

Request:

```json
{
  "username": "drish",
  "email": "drish@test.com",
  "password": "password123"
}
```

---

## Login

POST `/auth/login`

Request:

```json
{
  "email": "drish@test.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "TOKEN",
  "token_type": "bearer"
}
```

---

# Authorization

Protected APIs require:

```text
Authorization: Bearer <TOKEN>
```

---

# Job APIs

## Create One-Time Job

POST `/jobs/`

```json
{
  "job_name": "telegram-test",
  "job_type": "TELEGRAM_MESSAGE",
  "payload": {
    "chat_id": "5141275856",
    "message": "Hello from Chronos 🚀"
  },
  "schedule_type": "ONCE",
  "scheduled_time": "2026-05-12T23:59:00",
  "max_retries": 3
}
```

---

## Create Recurring Job

POST `/jobs/`

```json
{
  "job_name": "cron-test",
  "job_type": "TELEGRAM_MESSAGE",
  "payload": {
    "chat_id": "5141275856",
    "message": "Recurring Chronos Job ⏰"
  },
  "schedule_type": "CRON",
  "cron_expression": "* * * * *",
  "max_retries": 3
}
```

---

## Get All Jobs

GET `/jobs/`

---

## Get Single Job

GET `/jobs/{id}`

---

## Cancel Job

DELETE `/jobs/{id}`

---

## Reschedule Job

PUT `/jobs/{id}/reschedule`

```json
{
  "scheduled_time": "2026-05-13T00:10:00"
}
```

---

# Monitoring APIs

## Logs

GET `/jobs/logs/all`

---

## Health Check

GET `/jobs/health/check`

---

## Stats

GET `/jobs/stats/summary`

---

# Retry Mechanism

If execution fails:
1. retry_count increments
2. status becomes RETRYING
3. retries continue until max_retries reached
4. final status becomes FAILED

All failures are stored in:
- job_execution_logs

---

# Job Lifecycle

Success Flow:

```text
PENDING
   ↓
SCHEDULED
   ↓
RUNNING
   ↓
SUCCESS
```

Failure Flow:

```text
RUNNING
   ↓
FAILED
   ↓
RETRYING
   ↓
FAILED
```

---

# Scalability Considerations

The system is designed with scalability in mind.

Current design advantages:
- Generic job handlers
- Modular architecture
- Decoupled scheduler
- Persistent storage
- Background execution

Future improvements:
- Redis queues
- Multiple workers
- Kubernetes deployment
- Horizontal scaling
- Distributed schedulers

---

# Design Decisions

## Why FastAPI
- lightweight
- async support
- automatic Swagger docs

## Why APScheduler
- simple recurring scheduling
- cron support
- lightweight scheduler

## Why Generic Handlers
Allows new job types to be added independently.

## Why Docker
Provides isolated and reproducible deployment environments.

---

# Assignment Requirements Covered

| Requirement | Status |
|---|---|
| REST APIs | ✅ |
| One-time Jobs | ✅ |
| Recurring Jobs | ✅ |
| Job Management | ✅ |
| Retry Mechanism | ✅ |
| Logging & Monitoring | ✅ |
| Authentication | ✅ |
| Dockerized Deployment | ✅ |
| Scalable Architecture | ✅ |
| Generic Job Types | ✅ |

---

# Demo Flow

1. Register user
2. Login user
3. Create Telegram scheduled job
4. Receive Telegram message
5. Show logs API
6. Create recurring cron job
7. Cancel recurring job
8. Show monitoring APIs

---

# Future Improvements

- Email jobs
- Webhook jobs
- Distributed workers
- Queue-based execution
- Dashboard UI
- Kubernetes deployment

---

# Author

Chronos — Distributed Job Scheduling System
````
