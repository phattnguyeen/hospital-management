from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Update with your Render PostgreSQL URL
DATABASE_URL = "postgresql://phatnguyen:fFqMCm0RqQwdwq0rujX4IyNpHcCg8DA2@dpg-cvameh5svqrc73bvpveg-a.oregon-postgres.render.com/hospitalmanagement_txr6"

# Initialize database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get a new database session."""
    db: Session = SessionLocal()
    try:
        yield db  # Provide the session
    finally:
        db.close()  # Ensure the session is closed after use