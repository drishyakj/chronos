# Chronos

Chronos is a Distributed Job Scheduling System built using FastAPI, MySQL, SQLAlchemy, and APScheduler.

The system allows users to:
- schedule one-time jobs
- schedule recurring jobs
- manage jobs
- monitor executions
- retry failed jobs
- execute different job types using a generic handler architecture

The project is designed to demonstrate scalable backend system design concepts such as:
- distributed scheduling
- modular job execution
- retry handling
- monitoring
- extensibility
- REST API architecture

---

# Features

## Job Submission
- Immediate jobs
- Future scheduled jobs
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
- Automatic retry mechanism
- Failure logging
- Retry tracking

## Logging & Monitoring
- Execution logs
- Health monitoring APIs
- Statistics APIs

## Authentication
- JWT Authentication
- Protected APIs

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Scheduler | APScheduler |
| Authentication | JWT |
| Job Execution | Async Python |
| External Integration | Telegram Bot API |

---

# System Architecture

Chronos uses a modular handler-based architecture.

The scheduler itself is generic and does not contain business logic for individual job types.

Each job type has its own handler.

Example:

```python
JOB_HANDLERS = {
    "TELEGRAM_MESSAGE": TelegramHandler()
}
```

This allows future job types to be added without changing scheduler logic.

Future job types can include:
- EMAIL_NOTIFICATION
- FILE_BACKUP
- WEBHOOK_CALL
- REPORT_GENERATION
- DATABASE_CLEANUP

---

# Initial Job Type

Implemented:
- TELEGRAM_MESSAGE

The Telegram handler sends scheduled Telegram messages using Telegram Bot API.

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

Stores execution history and failures.

---

# Setup Instructions

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

ACCESS_TOKEN_EXPIRE_MINUTES=30

TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
```

---

# Telegram Bot Setup

## Create Telegram Bot

Open Telegram and search:

```text
BotFather
```

Create bot:

```text
/newbot
```

Copy generated bot token into `.env`

---

## Get Chat ID

Message your bot once.

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

# Swagger API Docs

Open:

```text
http://127.0.0.1:8000/docs
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

If a job execution fails:
1. retry_count increments
2. job status becomes RETRYING
3. retries continue until max_retries reached
4. final status becomes FAILED

All failures are stored in:
- job_execution_logs

---

# Job Lifecycle

```text
PENDING
   ↓
SCHEDULED
   ↓
RUNNING
   ↓
SUCCESS
```

Failure flow:

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

The project is designed with scalability in mind.

Key scalability concepts:
- Generic job handler architecture
- Modular scheduler design
- Decoupled execution engine
- Extensible payload-based jobs
- Background scheduling system

Future scalability improvements:
- Redis queues
- Multiple workers
- Docker deployment
- Kubernetes
- Distributed worker nodes
- Horizontal scaling

---

# Design Decisions

## Why FastAPI
- lightweight
- async support
- automatic Swagger docs
- easy REST API development

## Why APScheduler
- simple recurring scheduling
- cron support
- lightweight local scheduler

## Why Generic Handlers
Allows adding new job types without modifying scheduler core logic.

## Why MySQL
Reliable relational database with persistent storage.

---

# Assignment Requirements Covered

| Requirement | Status |
|---|---|
| REST APIs | ✅ |
| One-time Jobs | ✅ |
| Recurring Jobs | ✅ |
| Job Management | ✅ |
| Failure Handling | ✅ |
| Retry Mechanism | ✅ |
| Logging & Monitoring | ✅ |
| Authentication | ✅ |
| Scalable Design | ✅ |
| Generic Job Types | ✅ |

---

# Future Improvements

- Email Jobs
- File Processing Jobs
- Webhook Jobs
- Distributed Workers
- Docker Deployment
- Kubernetes
- Admin Dashboard
- Rate Limiting
- Queue-based execution
- Web UI

---

# Demo Flow

1. Register user
2. Login user
3. Create scheduled Telegram job
4. Receive Telegram message
5. Show execution logs
6. Create recurring cron job
7. Cancel recurring job
8. Show monitoring APIs

---

# Author

Chronos — Distributed Job Scheduling System