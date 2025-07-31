from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import ChatRoom, Message, User
from schemas import ChatRoomCreate, ChatRoomResponse, MessageResponse
from auth import get_current_user, require_admin

router = APIRouter(prefix="/rooms", tags=["chat rooms"])

@router.post("/", response_model=ChatRoomResponse, status_code=status.HTTP_201_CREATED)
def create_chat_room(
    room: ChatRoomCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)  # Only admins can create rooms
):
    # Check if room name already exists
    existing_room = db.query(ChatRoom).filter(ChatRoom.name == room.name).first()
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room with this name already exists"
        )
    
    db_room = ChatRoom(name=room.name, description=room.description)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    return db_room

@router.get("/", response_model=List[ChatRoomResponse])
def get_chat_rooms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rooms = db.query(ChatRoom).all()
    return rooms

@router.get("/{room_id}", response_model=ChatRoomResponse)
def get_chat_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    return room

@router.get("/{room_id}/messages", response_model=List[MessageResponse])
def get_room_messages(
    room_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if room exists
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Get messages with cursor-based pagination (newest first)
    messages = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(Message.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return messages

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)  # Only admins can delete rooms
):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    db.delete(room)
    db.commit()
    return None
