# Secure Asset Tracking and Log API

A RESTful API built with Python and FastAPI designed to handle inventory discovery and asset logging safely. This project implements a comprehensive security framework to protect endpoints against unauthorized data manipulation.

## Security Architecture

The application enforces data validation and user access controls across multiple layers:

- **Password Hashing:** User passwords are never stored in plain text. The system utilizes native Bcrypt signatures to compute individual cryptographic salted hashes before storing credentials in the database layer.
- **Session Authentication:** Implements industry-standard OAuth2 with JSON Web Tokens (JWT). Successful authentication issues an encrypted bearer session token that automatically expires after 30 minutes.
- **Dependency Injection:** The POST, PUT, and DELETE endpoints are locked behind an active session interceptor. FastAPI automatically validates the presence and signature of incoming bearer tokens before executing database actions, rejecting unauthorized access with a 401 Unauthorized status code.
- **Input Validation:** Built using Pydantic v2 schemas to enforce typing rules and block malicious data injection attempts before payloads hit the Object-Relational Mapper (ORM).

## Core Technologies and Dependencies

- **Framework:** FastAPI (Asynchronous ASGI Engine)
- **Database Engine:** SQLite (Persistent Relational Storage)
- **Object-Relational Mapper:** SQLAlchemy
- **Linting and Formatting:** Ruff
- **Static Type Checking:** Pyright

## Project Directory Structure

```text
APIStudy/
├── venv/                 # Local Virtual Environment (Hidden via .gitignore)
├── app.db                # SQLite Local Database File (Hidden via .gitignore)
├── auth.py               # Cryptographic Token & Hash Handlers
├── database.py           # SQLAlchemy Database Session Setup
├── main.py               # REST API Routing & Access-Control Dependencies
├── models.py             # Database Relational Table Schemas
└── .gitignore            # Git Tracking Exclusion Rules
```

## Installation and Deployment

1. **Activate the Virtual Environment:**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies:**

   ```powershell
   pip install fastapi uvicorn sqlalchemy pydantic bcrypt pyjwt python-multipart
   ```

3. **Launch the Live Server Engine:**

   ```powershell
   uvicorn main:app --reload
   ```

4. **Access API Documentation:**
   Navigate to `http://127.0.0` in your web browser to access the built-in Swagger UI and interact with the endpoints.
