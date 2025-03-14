from sqlalchemy import create_engine, Column, Integer, String, Text, Date, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://phatnguyen:fFqMCm0RqQwdwq0rujX4IyNpHcCg8DA2@dpg-cvameh5svqrc73bvpveg-a.oregon-postgres.render.com/hospitalmanagement_txr6"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")

def get_db():
    """Dependency to get a new database session."""
    from app.db.database import SessionLocal  # Move the import here to avoid circular import
    db: Session = SessionLocal()
    try:
        yield db  # Provide the session
    finally:
        db.close()  # Ensure the session is closed after use


