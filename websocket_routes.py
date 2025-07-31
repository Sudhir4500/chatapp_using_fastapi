from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import json
from datetime import datetime

from database import get_db
from models import User, ChatRoom, Message
from schemas import TokenData
from auth import verify_websocket_token
from websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Verify JWT token
    try:
        token_data: TokenData = verify_websocket_token(token)
    except HTTPException as e:
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    # Get user from database
    user = db.query(User).filter(User.username == token_data.username).first()
    if not user:
        await websocket.close(code=1008, reason="User not found")
        return
    
    # Check if room exists
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        await websocket.close(code=1008, reason="Room not found")
        return
    
    # Connect user to the room
    user_info = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role.value
    }
    
    await manager.connect(websocket, room_id, user_info)
    
    try:
        # Send recent messages to the newly connected user
        recent_messages = (
            db.query(Message)
            .filter(Message.room_id == room_id)
            .order_by(Message.timestamp.desc())
            .limit(20)
            .all()
        )
        
        # Send messages in chronological order
        for message in reversed(recent_messages):
            message_data = {
                "type": "message",
                "id": message.id,
                "content": message.content,
                "username": message.user.username,
                "user_id": message.user_id,
                "timestamp": message.timestamp.isoformat(),
                "room_id": message.room_id
            }
            await manager.send_personal_message(
                json.dumps(message_data, default=str), 
                websocket
            )
        
        # Send current active users list
        active_users = manager.get_active_users_in_room(room_id)
        users_data = {
            "type": "active_users",
            "users": active_users,
            "count": len(active_users)
        }
        await manager.broadcast_to_room(users_data, room_id)
        
        # Send join notification
        join_notification = {
            "type": "user_joined",
            "username": user.username,
            "message": f"{user.username} joined the room",
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.broadcast_to_room(join_notification, room_id)
        
        # Listen for messages
        while True:
            # Receive message from WebSocket
            data = await websocket.receive_text()
            message_json = json.loads(data)
            
            # Validate message content
            if "content" not in message_json or not message_json["content"].strip():
                continue
            
            # Save message to database
            db_message = Message(
                content=message_json["content"].strip(),
                user_id=user.id,
                room_id=room_id
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            # Prepare message for broadcast
            broadcast_message = {
                "type": "message",
                "id": db_message.id,
                "content": db_message.content,
                "username": user.username,
                "user_id": user.id,
                "timestamp": db_message.timestamp.isoformat(),
                "room_id": room_id
            }
            
            # Broadcast message to all connected clients in the room
            await manager.broadcast_to_room(broadcast_message, room_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
        # Send leave notification
        leave_notification = {
            "type": "user_left",
            "username": user.username,
            "message": f"{user.username} left the room",
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.broadcast_to_room(leave_notification, room_id)
        
        # Send updated active users list
        active_users = manager.get_active_users_in_room(room_id)
        users_data = {
            "type": "active_users",
            "users": active_users,
            "count": len(active_users)
        }
        await manager.broadcast_to_room(users_data, room_id)
        
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
