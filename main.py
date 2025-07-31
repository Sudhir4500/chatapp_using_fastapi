from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import engine
from models import Base
import auth_routes
import chat_routes
import websocket_routes

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Chat Application API",
    description="A FastAPI chat application with JWT authentication and WebSocket support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(websocket_routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Chat Application API",
        "docs": "/docs",
        "websocket": "/ws/{room_id}?token=your_jwt_token",
        "chat_client": "/chat"
    }

@app.get("/chat")
def get_chat_client():
    file_path = os.path.join(os.path.dirname(__file__), "chat_client.html")
    return FileResponse(file_path)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
