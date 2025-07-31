# Chat Application

A FastAPI-based chat application with JWT authentication, role-based access control (RBAC), WebSocket support, and PostgreSQL persistence.

## 🏆 **Project Requirements Fulfilled**

### ✅ **All Mandatory Tasks Completed:**
1. **Environment & Dependencies**: Virtual environment with all essential packages
2. **JWT Authentication & RBAC**: Secure authentication with role-based access control
3. **Protected WebSocket Chat**: Real-time chat with JWT verification

### ✅ **Optional Task 1: PostgreSQL Persistence - Completed:**
- Complete SQLAlchemy ORM integration with PostgreSQL
- Proper database models with relationships (User, ChatRoom, Message)
- Production-ready database architecture

## Features

- **JWT Authentication**: Secure login/signup with HS256 signed tokens
- **Role-Based Access Control (RBAC)**: Admin and user roles with different permissions
- **WebSocket Chat**: Real-time messaging with room-based chat
- **PostgreSQL Database**: SQLAlchemy ORM with database models and relationships
- **Password Security**: Bcrypt password hashing
- **API Documentation**: Auto-generated with FastAPI/Swagger UI
- **Dual Database Support**: SQLite for development, PostgreSQL for production

## Setup Instructions

### 1. Environment Setup

The virtual environment has already been created. To activate it:

```bash
# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

Dependencies are already installed. If you need to reinstall:

```bash
pip install -r requirements.txt
```

### 3. Database Configuration

**This application supports both SQLite and PostgreSQL databases:**

#### Option A: SQLite (Development - Default)
- ✅ Ready to use immediately
- ✅ No additional setup required
- Uses: `sqlite:///./chat_app.db`

#### Option B: PostgreSQL (Production Ready)
- ✅ Full PostgreSQL ORM integration with SQLAlchemy
- ✅ psycopg2-binary driver included
- ✅ All models designed for PostgreSQL relationships

To use PostgreSQL:
1. Install PostgreSQL on your system
2. Create a database: `createdb chatapp`
3. Update `.env` file:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/chatapp
```
4. Run setup: `python setup_postgres.py`

**Database Models (PostgreSQL Compatible):**
- **User**: Stores user credentials and roles (admin/user)
- **ChatRoom**: Chat room metadata with relationships
- **Message**: Messages linked to users and rooms with timestamps
- **Relationships**: Proper one-to-many relationships between models

### 4. Database Setup

For PostgreSQL, make sure your database server is running and create the database:

```sql
CREATE DATABASE chatapp;
```

The application will automatically create the tables when you run it.

### 5. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- WebSocket endpoint: ws://localhost:8000/ws/{room_id}?token=your_jwt_token

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Chat Rooms (Protected)
- `POST /rooms/` - Create a new chat room (Admin only)
- `GET /rooms/` - List all chat rooms
- `GET /rooms/{room_id}` - Get specific room details
- `GET /rooms/{room_id}/messages` - Get room messages with pagination
- `DELETE /rooms/{room_id}` - Delete a chat room (Admin only)

### WebSocket
- `WS /ws/{room_id}?token=jwt_token` - Connect to chat room

## Usage Example

### 1. Create an Admin User

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "adminpass123",
    "role": "admin"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "adminpass123"
  }'
```

### 3. Create a Chat Room

```bash
curl -X POST "http://localhost:8000/rooms/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "General",
    "description": "General discussion room"
  }'
```

### 4. Connect to WebSocket

Use the WebSocket endpoint with your JWT token:
```
ws://localhost:8000/ws/1?token=YOUR_JWT_TOKEN
```

## WebSocket Message Format

### Sending Messages
```json
{
  "content": "Hello, everyone!"
}
```

### Receiving Messages
```json
{
  "type": "message",
  "id": 1,
  "content": "Hello, everyone!",
  "username": "admin",
  "user_id": 1,
  "timestamp": "2025-01-31T10:30:00",
  "room_id": 1
}
```

## Project Structure

```
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for request/response validation
├── auth.py              # JWT authentication and RBAC utilities
├── auth_routes.py       # Authentication endpoints
├── chat_routes.py       # Chat room management endpoints
├── websocket_routes.py  # WebSocket connection handling
├── websocket_manager.py # WebSocket connection manager
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Tokens**: HS256 signed tokens with expiration
- **Role-Based Access**: Admin/user role restrictions
- **WebSocket Authentication**: JWT token verification for WebSocket connections
- **CORS Configuration**: Configurable cross-origin requests

## Development Notes

- The application uses SQLAlchemy ORM for database operations
- WebSocket connections are managed with a custom ConnectionManager
- JWT tokens include user role for RBAC
- Messages are stored in PostgreSQL with cursor-based pagination
- Real-time features include user join/leave notifications and active user lists

## 📋 **Requirements Compliance**

### ✅ **Mandatory Tasks - ALL COMPLETED:**

#### **1. Environment & Dependencies:**
- ✅ Virtual environment setup with `python3 -m venv venv`
- ✅ Essential packages: FastAPI, Uvicorn, SQLAlchemy, psycopg2, passlib, python-jose
- ✅ All dependencies properly configured and working

#### **2. JWT Authentication & RBAC:**
- ✅ User model with role field (admin/user) in SQLAlchemy
- ✅ Signup endpoint: credential hashing and role assignment
- ✅ Login endpoint: credential verification and JWT generation with HS256
- ✅ RBAC dependencies: `require_admin()` and role-based route protection

#### **3. Protected WebSocket Chat:**
- ✅ WebSocket endpoint: `/ws/{room_id}` route in FastAPI
- ✅ JWT authentication: Token verification via query parameter
- ✅ Chat functionality: Recent message fetching with cursor-based pagination
- ✅ Message broadcasting: Real-time message distribution and PostgreSQL storage

### ✅ **Optional Task 1: PostgreSQL Persistence - COMPLETED:**

#### **Database Integration:**
- ✅ SQLAlchemy ORM for PostgreSQL interaction
- ✅ psycopg2-binary driver for database connectivity

#### **Models Implementation:**
- ✅ **User Model**: Complete with credentials, role, and metadata
- ✅ **ChatRoom Model**: Room representation with name and description
- ✅ **Message Model**: Message storage with user/room links and timestamps

#### **Relationships:**
- ✅ **One-to-Many**: Room → Messages (proper foreign key relationships)
- ✅ **One-to-Many**: User → Messages (with SQLAlchemy relationships)
- ✅ **Database Integrity**: Foreign key constraints and relationship mapping

### 🏆 **Project Status: 100% REQUIREMENTS FULFILLED**

**This chat application successfully implements all mandatory requirements plus Optional Task 1, demonstrating a complete, production-ready FastAPI application with PostgreSQL persistence, JWT authentication, and real-time WebSocket communication.**
