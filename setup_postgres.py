"""
Setup script for PostgreSQL database
Run this to create the database and tables
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from database import Base, DATABASE_URL
from models import User, ChatRoom, Message

def create_database():
    """Create the chatapp database if it doesn't exist"""
    try:
        # Extract database name from URL
        db_name = DATABASE_URL.split('/')[-1]
        
        # Connect to PostgreSQL server (without specific database)
        server_url = DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
        
        engine = create_engine(server_url)
        
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.fetchone():
                # Create database
                conn.execute(text("COMMIT"))  # End current transaction
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"✅ Database '{db_name}' created successfully!")
            else:
                print(f"✅ Database '{db_name}' already exists!")
                
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

def create_tables():
    """Create all tables in the database"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_connection():
    """Test the database connection"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 To fix this:")
        print("1. Make sure PostgreSQL is running")
        print("2. Update the DATABASE_URL in .env with correct username/password")
        print("3. Or use SQLite by changing DATABASE_URL to: sqlite:///./chat_app.db")
        return False

if __name__ == "__main__":
    print("🚀 Setting up PostgreSQL for Chat Application...")
    print(f"📍 Database URL: {DATABASE_URL}")
    
    if test_connection():
        if create_database():
            if create_tables():
                print("\n🎉 PostgreSQL setup completed successfully!")
                print("You can now run: python main.py")
            else:
                print("\n❌ Failed to create tables")
        else:
            print("\n❌ Failed to create database")
    else:
        print("\n❌ PostgreSQL setup failed")
