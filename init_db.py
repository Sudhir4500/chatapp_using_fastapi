"""
Initialization script to create sample data for the chat application
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, ChatRoom, UserRole
from auth import get_password_hash

# Create all tables
Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.admin
            )
            db.add(admin_user)
            print("Created admin user: username='admin', password='admin123'")
        
        # Check if regular user exists
        regular_user = db.query(User).filter(User.username == "user1").first()
        if not regular_user:
            # Create regular user
            regular_user = User(
                username="user1",
                email="user1@example.com",
                hashed_password=get_password_hash("user123"),
                role=UserRole.user
            )
            db.add(regular_user)
            print("Created regular user: username='user1', password='user123'")
        
        # Check if sample rooms exist
        general_room = db.query(ChatRoom).filter(ChatRoom.name == "General").first()
        if not general_room:
            # Create sample chat rooms
            general_room = ChatRoom(
                name="General",
                description="General discussion room for everyone"
            )
            db.add(general_room)
            print("Created 'General' chat room")
        
        tech_room = db.query(ChatRoom).filter(ChatRoom.name == "Tech Talk").first()
        if not tech_room:
            tech_room = ChatRoom(
                name="Tech Talk",
                description="Discuss technology and programming"
            )
            db.add(tech_room)
            print("Created 'Tech Talk' chat room")
        
        random_room = db.query(ChatRoom).filter(ChatRoom.name == "Random").first()
        if not random_room:
            random_room = ChatRoom(
                name="Random",
                description="Off-topic discussions and random chat"
            )
            db.add(random_room)
            print("Created 'Random' chat room")
        
        db.commit()
        print("\nDatabase initialization completed!")
        print("\nSample credentials:")
        print("Admin - username: admin, password: admin123")
        print("User  - username: user1, password: user123")
        print("\nSample chat rooms created with IDs 1, 2, 3")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
