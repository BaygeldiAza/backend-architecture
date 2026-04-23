# Backend Architecture (FastAPI) — Junior Guide

## Goal

This project teaches you the **basics of backend development** using FastAPI with a clean and scalable structure.

You will learn:

* How backend folders are organized
* How requests flow through the system
* How to separate logic properly

---

## 🧠 Basic Idea (Simple Explanation)

Think of backend like a restaurant:

* **API (routes)** → waiter (takes request)
* **Service** → chef (does the work)
* **Database** → storage (ingredients)
* **Schemas** → rules (what is allowed)

Flow:

Client → API → Service → Database → Response

---

## 📁 Project Structure

```
app/
│
├── main.py                # Entry point
│
├── api/
│   └── v1/
│       └── users.py      # Routes
│
├── models/
│   └── user.py           # Database model
│
├── schemas/
│   └── user.py           # Validation
│
├── services/
│   └── user_service.py   # Business logic
│
├── db/
│   └── database.py       # DB connection
│
└── core/
    └── config.py         # Settings
```

---

## 🔁 Request Flow Example

User sends:

```
POST /users
```

Steps:

1. `users.py` receives request
2. `schemas/user.py` validates data
3. `user_service.py` processes logic
4. `user.py` model saves to DB
5. Response returned

---

## ⚙️ Setup Instructions

### 1. Create virtual environment

```
python -m venv venv
```

### 2. Activate

```
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install fastapi uvicorn sqlalchemy
```

### 4. Run server

```
uvicorn app.main:app --reload
```

---

## 🚀 Features in this project

* Create user
* Get all users
* Simple in-memory DB (for learning)

---

## 🧱 Code Implementation

### app/main.py

```python
from fastapi import FastAPI
from app.api.v1 import users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
```

---

### app/api/v1/users.py

```python
from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.services.user_service import create_user, get_users

router = APIRouter()

@router.post("/")
def create(user: UserCreate):
    return create_user(user)

@router.get("/")
def read():
    return get_users()
```

---

### app/schemas/user.py

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
```

---

### app/models/user.py

```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
```

---

### app/services/user_service.py

```python
from app.models.user import User

# Fake database
users_db = []

def create_user(user_data):
    user = User(user_data.name, user_data.email)
    users_db.append(user.__dict__)
    return user

def get_users():
    return users_db
```

---

### app/db/database.py

```python
# For now, we use a simple list instead of real DB
# Later you will replace this with SQLAlchemy
```

---

### app/core/config.py

```python
class Settings:
    APP_NAME = "Backend Architecture"

settings = Settings()
```

---

## ⚠️ Important Notes

* This is **basic level**, not production
* No authentication yet
* No real database yet

---

## 🔐 Upgrade: Database + Auth (Junior → Intermediate Bridge)

Now we upgrade your project with:

* MySQL database
* SQLAlchemy ORM
* User model (real DB)
* Authentication (JWT)

---

## 📦 Install dependencies

```
pip install fastapi uvicorn sqlalchemy pymysql python-jose passlib[bcrypt]
```

---

## ⚙️ Database Setup (MySQL)

### app/db/database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/testdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## 🧱 Model (Database Table)

### app/models/user.py

```python
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
```

### Explanation:

* `id` → unique identifier (primary key)
* `name` → user name
* `email` → must be unique (no duplicates)
* `password` → hashed password (never plain text)

---

## 📥 Schemas (Validation Layer)

### app/schemas/user.py

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
```

### Explanation:

* `UserCreate` → input validation (request body)
* `UserResponse` → what you return to client
* `EmailStr` → validates email format
* `orm_mode` → allows SQLAlchemy model → JSON conversion

---

## 🔐 Security (Password Hashing)

### app/core/security.py

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
```

---

## 🔑 JWT Authentication

### app/core/auth.py

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 🧠 Service Layer (Business Logic)

### app/services/user_service.py

```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password


def create_user(db: Session, user_data):
    hashed = hash_password(user_data.password)
    user = User(name=user_data.name, email=user_data.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()
```

---

## 🌐 API Layer (Routes)

### app/api/v1/users.py

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users
from app.db.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/", response_model=list[UserResponse])
def read(db: Session = Depends(get_db)):
    return get_users(db)
```

---

## 🔄 Updated Flow (Real Backend)

Client → API → Schema → Service → Model → Database → Response

---

## ⚠️ Important (Reality Check)

Still missing:

* Login endpoint
* Token verification middleware
* Refresh tokens
* Production config

---

## 🚀 Next Steps

After this stage:

* Add login endpoint
* Protect routes with JWT
* Add roles/permissions
* Move config to .env

---

## 🎯 Final Advice

Now you are not just "learning backend".

You are building a **real backend foundation**.

Understand every layer — that’s what separates beginners from engineers.
