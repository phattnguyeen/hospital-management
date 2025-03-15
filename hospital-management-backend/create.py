from sqlalchemy import create_engine, Column, Integer, String, Text, Date, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# Update with your Render PostgreSQL URL
DATABASE_URL = "postgresql://phatnguyen:fFqMCm0RqQwdwq0rujX4IyNpHcCg8DA2@dpg-cvameh5svqrc73bvpveg-a.oregon-postgres.render.com/hospitalmanagement_txr6"

# Initialize database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Patient table
class Patient(Base):
    __tablename__ = "patient"

    patient_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    age = Column(Integer, CheckConstraint("age >= 0"))
    phone_no = Column(String(15), unique=True)
    address = Column(Text)
    patient_type = Column(String(50))
    sex = Column(String(10), CheckConstraint("sex IN ('Male', 'Female', 'Other')"))
    admit_date = Column(Date)
    discharge_date = Column(Date, CheckConstraint("discharge_date IS NULL OR discharge_date >= admit_date"))

# Create tables in the database
def create_tables():
    """Ensure tables are created in the database."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

# Insert sample patients into the database
def add_sample_patients():
    """Insert sample patient records into the database."""
    session = SessionLocal()
    try:
        patients = [
            Patient(
                username="alex",
                name="John Doe",
                password="$2b$12$JDqU9zlBGOsrarZ2XBDk2uoOowU8X3qpZTgjz43sHQIw3TYIhHTCa",
                age=30,
                phone_no="1234567890",
                address="123 Main St, New York",
                patient_type="Outpatient",
                sex="Male",
                admit_date=func.current_date(),
                discharge_date=None
            ),
            Patient(
                username="jane_smith",
                name="Jane Smith",
                password="password456",
                age=25,
                phone_no="0987654321",
                address="456 Elm St, California",
                patient_type="Inpatient",
                sex="Female",
                admit_date=func.current_date(),
                discharge_date=None
            )
        ]
        
        session.add_all(patients)
        session.commit()
        print("Sample patient records added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding sample patients: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    create_tables()
    add_sample_patients()
