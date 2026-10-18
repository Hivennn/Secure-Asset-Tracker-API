# Secure Asset Tracking and Log API & Dashboard

A full-stack network inventory and asset tracking application powered by a FastAPI RESTful backend and a responsive, vanilla JavaScript frontend dashboard. The project implements a multi-layer security architecture with bcrypt password hashing and JWT-based session protection.

---

## Features

- **User Authentication:** User registration and token-based login utilizing industry-standard OAuth2 password flow with JWT (JSON Web Tokens).
- **Password Security:** Cryptographically secure password hashing using salted bcrypt hashes.
- **Protected CRUD Operations:** Endpoints for creating, viewing, updating, and deleting infrastructure assets are protected behind authentication dependencies.
- **Input Validation:** Strict payload validation via Pydantic v2 data models.
- **Interactive Web Dashboard:** Clean, responsive frontend interface with live session management, asset logging, and inventory table views.
- **Interactive API Documentation:** Auto-generated OpenAPI / Swagger UI documentation.

---

## Security Architecture

The application enforces data validation and access controls across multiple layers:

- **Password Hashing:** User passwords are never stored in plain text. Native bcrypt computes cryptographic salted hashes before credentials hit SQLite storage.
- **Session Authentication:** Generates HS256-signed JSON Web Tokens (`access_token`) expiring after 30 minutes.
- **Dependency Injection Guard:** Endpoints accessing asset data require a valid `Bearer` token passed in the `Authorization` header, validated by FastAPI's `Depends(get_current_user)`.
- **CORS Configuration:** Enables secure communication between local frontend files and backend API endpoints.

---

## Core Technologies & Dependencies

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous ASGI Engine)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Database Engine:** SQLite (Local relational database)
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Security & Tokens:** `bcrypt`, `PyJWT`
- **Frontend:** HTML5, Modern Vanilla CSS, Vanilla JavaScript (Fetch API)

---

## Project Directory Structure

```text
APIStudy/
├── frontend/
│   ├── app.js            # Frontend application logic, state, and API requests
│   ├── index.html        # Main dashboard and authentication UI
│   └── styles.css        # Responsive layout and component styling
├── app.db                # SQLite database file (created automatically)
├── auth.py               # Cryptographic token creation and password hashing
├── database.py           # SQLAlchemy database engine and session setup
├── main.py               # REST API endpoints, CORS, and auth dependencies
├── models.py             # SQLAlchemy ORM table models (users & assets)
├── README.md             # Project documentation
└── venv/                 # Python virtual environment (ignored by git)
```

---

## API Endpoints Reference

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/` | No | Health check and welcome message |
| `POST` | `/register` | No | Register a new user account |
| `POST` | `/login` | No | Authenticate user and receive Bearer JWT |
| `GET` | `/assets` | **Yes** | Fetch all registered network assets |
| `GET` | `/assets/{asset_id}` | **Yes** | Fetch specific asset by ID |
| `POST` | `/assets` | **Yes** | Create a new asset entry |
| `PUT` | `/assets/{asset_id}` | **Yes** | Update an existing asset by ID |
| `DELETE` | `/assets/{asset_id}` | **Yes** | Delete an asset entry by ID |

---

## Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install fastapi uvicorn sqlalchemy pydantic bcrypt pyjwt python-multipart
```

### 4. Run the Backend API
Start the Uvicorn ASGI server with automatic reload:
```powershell
uvicorn main:app --reload
```
The server will be available at: `http://127.0.0.1:8000`

### 5. Open the Frontend Dashboard
Open `frontend/index.html` directly in your web browser, or serve it using Python's built-in HTTP server or VS Code Live Server.

### 6. Interactive API Documentation
Navigate to `http://127.0.0.1:8000/docs` in your web browser to explore and test all endpoints using the built-in Swagger UI.
