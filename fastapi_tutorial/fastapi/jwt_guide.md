# 🔑 Complete Guide to JWT Authentication in FastAPI

Welcome to the comprehensive study guide on **JSON Web Tokens (JWT)**, password hashing, and implementing stateless authentication in FastAPI applications.

---

## 📋 Table of Contents
1. [What is a JSON Web Token (JWT)?](#1-what-is-a-json-web-token-jwt)
2. [Session-Based vs. Token-Based (JWT) Authentication](#2-session-based-vs-token-based-jwt-authentication)
3. [Anatomy of a JWT Token](#3-anatomy-of-a-jwt-token)
4. [Security Fundamentals & Password Hashing](#4-security-fundamentals--password-hashing)
5. [The Complete JWT Authentication Lifecycle](#5-the-complete-jwt-authentication-lifecycle)
6. [Step-by-Step FastAPI Implementation](#6-step-by-step-fastapi-implementation)
7. [Testing JWT in Swagger UI & Postman](#7-testing-jwt-in-swagger-ui--postman)
8. [Common Pitfalls & Best Practices](#8-common-pitfalls--best-practices)

---

## 1. What is a JSON Web Token (JWT)?

A **JSON Web Token (JWT)** (defined in [RFC 7519](https://tools.ietf.org/html/rfc7519)) is an open, industry-standard method for representing claims securely between two parties.

In simple terms, a JWT is a **digitally signed string** containing JSON data that allows a client (e.g. React frontend, mobile app) to prove its identity to a backend server.

### Key Characteristics:
- **Stateless:** The server does not need to store active sessions in a database or memory. All information needed to identify the user is encoded directly inside the token.
- **Self-Contained:** The token carries user information (like `user_id` and `email`) and expiration metadata.
- **Tamper-Proof:** Signed using a secret key (HMAC SHA-256) or public/private key pair (RSA/ECDSA). If a client modifies even one character of the token, the server signature verification will fail.

---

## 2. Session-Based vs. Token-Based (JWT) Authentication

| Feature | Session-Based Authentication | Token-Based (JWT) Authentication |
| :--- | :--- | :--- |
| **State Storage** | **Stateful:** Server keeps session IDs in RAM (Redis/Memcached) or DB. | **Stateless:** Server stores nothing. Token is held by the client. |
| **Scalability** | Harder to scale horizontally (requires shared session store). | Easy to scale across multiple servers/microservices. |
| **Cross-Domain** | Cookies can be restricted by CORS / domain policies. | Tokens are sent via HTTP headers (`Authorization: Bearer <token>`). |
| **Revocation** | Easy (delete session from server database). | Harder (tokens remain valid until expired, unless blacklisted). |

---

## 3. Anatomy of a JWT Token

A JWT string consists of **three parts separated by dots (`.`)**:

$$\text{HEADER} . \text{PAYLOAD} . \text{SIGNATURE}$$

Example token:
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJuYW1lIjoiSm9obiIsImV4cCI6MTcwMDAwMDAwMH0.signatureBytesHere...`

---

### Part 1: Header
Contains metadata about the token format and algorithm used for signing.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
* **`alg`**: The algorithm used (e.g. `HS256` for HMAC SHA-256).
* **`typ`**: Type of token (`JWT`).

*This JSON object is Base64URL encoded.*

---

### Part 2: Payload (Claims)
Contains user data and token metadata.

```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "exp": 1700000000
}
```

#### Reserved Claims (Standardized):
- `exp` (Expiration Time): Unix timestamp after which token expires.
- `sub` (Subject): Identifies the principal (e.g., user ID).
- `iat` (Issued At): Timestamp when token was created.

#### Custom Claims:
- You can add your own fields such as `name`, `email`, `role` (e.g. `"role": "admin"`).

> ⚠️ **CRITICAL WARNING:** The payload is **Base64URL encoded, NOT encrypted**. Anyone who intercepts the token can decode it and read its JSON contents! **Never store sensitive data (passwords, credit cards, SSN) inside a JWT payload.**

---

### Part 3: Signature
Calculated by hashing the encoded header, encoded payload, and a secret key using the specified algorithm:

```text
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  SECRET_KEY
)
```

If anyone attempts to alter the `user_id` in the payload from `1` to `2`, the signature will no longer match the modified payload when verified on the server using `SECRET_KEY`.

---

## 4. Security Fundamentals & Password Hashing

Before issuing a JWT token, users must log in with a password. Passwords **must never be stored in plain text**.

### Password Hashing Strategy:
1. **Pre-hashing with SHA-256:** Converts passwords of any length into a fixed 64-character string (prevents bcrypt 72-byte truncation vulnerabilities).
2. **Salting & Bcrypt Hashing:** Uses `bcrypt.gensalt()` to generate a unique random salt and hash the password.

```python
import bcrypt
import hashlib

def hash_password(password: str) -> bytes:
    # 1. Pre-hash password with SHA-256
    pre_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # 2. Hash with bcrypt + salt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pre_hashed.encode('utf-8'), salt)

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    pre_hashed = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return bcrypt.checkpw(pre_hashed.encode('utf-8'), hashed_password)
```

---

## 5. The Complete JWT Authentication Lifecycle

```text
┌────────┐                               ┌────────┐                              ┌──────────┐
│ Client │                               │ Server │                              │ Database │
└───┬────┘                               └───┬────┘                              └────┬─────┘
    │                                        │                                        │
    │ 1. POST /auth/register                 │                                        │
    ├───────────────────────────────────────>│ 2. Hash password                       │
    │    (name, email, password)             │───────────────────────────────────────>│
    │                                        │    Save (name, email, hashed_password) │
    │ 3. Response: "User Registered"         │                                        │
    │<───────────────────────────────────────┤                                        │
    │                                        │                                        │
    │ 4. POST /auth/login                    │                                        │
    ├───────────────────────────────────────>│ 5. Fetch user by email                 │
    │    (email, password)                   │───────────────────────────────────────>│
    │                                        │<───────────────────────────────────────┤
    │                                        │ 6. verify_password()                   │
    │                                        │ 7. Generate JWT access_token           │
    │ 8. Response: { access_token, bearer }  │                                        │
    │<───────────────────────────────────────┤                                        │
    │                                        │                                        │
    │ 9. GET /user/profile                   │                                        │
    │    Header: Authorization: Bearer <JWT> │                                        │
    ├───────────────────────────────────────>│ 10. verify_token(JWT)                 │
    │                                        │ 11. Decode payload & extract user      │
    │ 12. Response: { "user": payload }      │                                        │
    │<───────────────────────────────────────┤                                        │
```

---

## 6. Step-by-Step FastAPI Implementation

### Prerequisites: Install Required Libraries
```bash
pip install "fastapi[all]" python-jose[cryptography] passlib bcrypt
```

---

### Step 6.1: JWT Handler (`jwt_handler.py`)
Responsible for creating and verifying JWT tokens using `python-jose`.

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException

# CONFIGURATION
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """Generates a signed JWT access token with an expiration claim."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Decodes and validates a JWT token signature and expiration."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
```

---

### Step 6.2: Security Dependency (`auth.py`)
Responsible for extracting the bearer token from HTTP headers and verifying identity.

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt_handler import verify_token

# Connects FastAPI Swagger UI to authentication endpoint
oauth2scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2scheme)) -> dict:
    """Extracts token from header, validates it, and returns payload."""
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    return payload
```

---

### Step 6.3: Authentication Router (`auth_router.py`)
Handles `/auth/register` and `/auth/login` endpoints.

```python
from fastapi import APIRouter, HTTPException
from schemas.models import UserRegister, UserLogin
from database.database import get_connection
from utils import hash_password, verify_password
from jwt_handler import create_access_token

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_pw = hash_password(user.password)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                   (user.name, user.email, hashed_pw))
    conn.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (user.email,))
    existing_user = cursor.fetchone()

    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token(data={"user_id": existing_user["id"], "name": existing_user["name"]})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

---

### Step 6.4: Protected User Router (`user_router.py`)
Demonstrates protecting routes using `Depends(get_current_user)`.

```python
from fastapi import APIRouter, Depends
from auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Access Granted",
        "user_profile": current_user
    }
```

---

## 7. Testing JWT in Swagger UI & Postman

### Testing in Swagger UI (`/docs`):
1. Start application: `uvicorn main3:app --reload`
2. Open browser: `http://127.0.0.1:8000/docs`
3. Register a user via `POST /auth/register`.
4. Log in via `POST /auth/login` and copy the returned `access_token`.
5. Click the green **"Authorize"** button at top right of `/docs`.
6. Paste the token into the Value box and click **Authorize**.
7. Execute `GET /user/profile` — Swagger will automatically include `Authorization: Bearer <token>`.

### Testing with cURL:
```bash
curl -X GET "http://127.0.0.1:8000/user/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 8. Common Pitfalls & Best Practices

1. 🔑 **Hardcoding Secret Keys:**
   - **Bad:** `SECRET_KEY = "123456"` in python files.
   - **Good:** Use environment variables (`os.getenv("SECRET_KEY")` or `.env` files).

2. 🔓 **Sensitive Data Leakage:**
   - **Bad:** Putting passwords, hashes, or social security numbers into JWT payload.
   - **Good:** Only include non-sensitive identifiers like `user_id`, `email`, `role`.

3. ⏳ **Infinite Expiration Time:**
   - **Bad:** Setting token expiration to 10 years or omitting `exp`.
   - **Good:** Set short-lived access tokens (15–30 minutes) and use Refresh Tokens for long sessions.

4. 🔒 **HTTPS Transmission:**
   - Always serve JWT-authenticated APIs over **HTTPS** in production so tokens cannot be snooped over public networks.
