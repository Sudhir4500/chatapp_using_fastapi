from typing import Dict, List, Set
from fastapi import WebSocket
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        # Store active connections by room_id
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Store user info for each connection
        self.connection_users: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, room_id: int, user_info: dict):
        await websocket.accept()
        
        # Add room if it doesn't exist
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        
        # Add connection to room
        self.active_connections[room_id].add(websocket)
        self.connection_users[websocket] = {
            "user_id": user_info["user_id"],
            "username": user_info["username"],
            "room_id": room_id
        }
        
        print(f"User {user_info['username']} connected to room {room_id}")
    
    def disconnect(self, websocket: WebSocket):
        # Find and remove the connection
        user_info = self.connection_users.get(websocket)
        if user_info:
            room_id = user_info["room_id"]
            if room_id in self.active_connections:
                self.active_connections[room_id].discard(websocket)
                
                # Remove empty room
                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]
            
            del self.connection_users[websocket]
            print(f"User {user_info['username']} disconnected from room {room_id}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast_to_room(self, message: dict, room_id: int):
        if room_id in self.active_connections:
            message_str = json.dumps(message, default=str)
            connections_to_remove = []
            
            for connection in self.active_connections[room_id].copy():
                try:
                    await connection.send_text(message_str)
                except:
                    # Connection is closed, mark for removal
                    connections_to_remove.append(connection)
            
            # Remove closed connections
            for connection in connections_to_remove:
                self.disconnect(connection)
    
    def get_room_connections_count(self, room_id: int) -> int:
        return len(self.active_connections.get(room_id, set()))
    
    def get_active_users_in_room(self, room_id: int) -> List[dict]:
        if room_id not in self.active_connections:
            return []
        
        users = []
        for connection in self.active_connections[room_id]:
            user_info = self.connection_users.get(connection)
            if user_info:
                users.append({
                    "user_id": user_info["user_id"],
                    "username": user_info["username"]
                })
        return users

# Global connection manager instance
manager = ConnectionManager()
