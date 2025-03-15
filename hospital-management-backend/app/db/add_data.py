from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.patient import Patient
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Create a new database session
db: Session = SessionLocal()

# Add data to the Patient table
new_patient = Patient(
    username="johndoe",
    name="John Doe",
    age=30,
    password=get_password_hash("securepassword"),
    phone_no="123-456-7890",
    address="123 Main St",
    patient_type="Inpatient",
    sex="Male",
    admit_date="2025-03-04",
    discharge_date="2025-03-10"
)

db.add(new_patient)
db.commit()
db.refresh(new_patient)
print(f"Patient {new_patient.name} added successfully")

# Close the database session
db.close()