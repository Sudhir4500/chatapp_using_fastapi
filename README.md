# Chat Application

A FastAPI-based chat application with JWT authentication, role-based access control (RBAC), and WebSocket support.

## Features

- **JWT Authentication**: Secure login/signup with HS256 signed tokens
- **Role-Based Access Control (RBAC)**: Admin and user roles with different permissions
- **WebSocket Chat**: Real-time messaging with room-based chat
- **PostgreSQL Database**: SQLAlchemy ORM with database models
- **Password Security**: Bcrypt password hashing
- **API Documentation**: Auto-generated with FastAPI/Swagger UI

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

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit the `.env` file with your database configuration:

- For PostgreSQL: Update the `DATABASE_URL` with your credentials
- For SQLite (development): Uncomment the SQLite URL and comment the PostgreSQL URL

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
