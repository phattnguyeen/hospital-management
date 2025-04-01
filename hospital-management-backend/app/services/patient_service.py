from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

def get_patient_by_id(db: Session, patient_id: str):
    """Fetch a patient by their ID."""
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()

def create_patient(db: Session, patient_data: PatientCreate):
    """Creates a new patient record."""
    new_patient = Patient(
        full_name=patient_data.full_name,
        birth_date=patient_data.birth_date,
        gender=patient_data.gender,
        address=patient_data.address,
        phone_number=patient_data.phone_number,
        email=patient_data.email,
        medical_history=patient_data.medical_history,
    )
    db.add(new_patient)
    db.flush()  # ✅ Force SQLAlchemy to assign patient_id before commit
    print(f"Generated Patient ID (Before Commit): {new_patient.patient_id}")  # Debugging
    db.commit()
    db.refresh(new_patient)  # ✅ Fetch updated patient_id

    return new_patient


def update_patient(db: Session, patient_id: str, patient_data: PatientUpdate):
    """Updates an existing patient record."""
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return None

    update_data = patient_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: str):
    """Deletes a patient record."""
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return None

    db.delete(db_patient)
    db.commit()
    return db_patient