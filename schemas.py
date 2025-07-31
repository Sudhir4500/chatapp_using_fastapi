from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import UserRole

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.user

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Chat room schemas
class ChatRoomBase(BaseModel):
    name: str
    description: Optional[str] = None

class ChatRoomCreate(ChatRoomBase):
    pass

class ChatRoomResponse(ChatRoomBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    room_id: int

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    user_id: int
    room_id: int
    user: UserResponse
    
    class Config:
        from_attributes = True

class WebSocketMessage(BaseModel):
    content: str
    room_id: int
