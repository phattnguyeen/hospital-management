# services/patient_service.py

from sqlalchemy.orm import Session
from uuid import UUID
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a plain password matches a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_patient_by_id(db: Session, patient_id: UUID):
    """Fetch a patient by their ID."""
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()

def get_patient_by_username(db: Session, username: str):
    """Fetch a patient by their username."""
    return db.query(Patient).filter(Patient.username == username).first()

def create_patient(db: Session, patient_data: PatientCreate):
    """Creates a new patient record."""
    hashed_password = get_password_hash(patient_data.password)
    new_patient = Patient(
        username=patient_data.username,
        name=patient_data.name,
        age=patient_data.age,
        password=hashed_password,
        phone_no=patient_data.phone_no,
        address=patient_data.address,
        patient_type=patient_data.patient_type,
        sex=patient_data.sex,
        admit_date=patient_data.admit_date,
        discharge_date=patient_data.discharge_date
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

def update_patient(db: Session, patient_id: UUID, patient_data: PatientUpdate):
    """Updates an existing patient record."""
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return None

    update_data = patient_data.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: UUID):
    """Deletes a patient record."""
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return None

    db.delete(db_patient)
    db.commit()
    return db_patient
