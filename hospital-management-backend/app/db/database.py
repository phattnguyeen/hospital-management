from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Update with your Render PostgreSQL URL
DATABASE_URL = "postgresql://hmsdb_owner:npg_9IzgxcpTou6D@ep-proud-snowflake-a5e4oyfd-pooler.us-east-2.aws.neon.tech/hmsdb?sslmode=require"

# Initialize database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get a new database session."""
    db: Session = SessionLocal()
    try:
        yield db  
    finally:
        db.close()  