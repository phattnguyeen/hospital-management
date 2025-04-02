from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate

def get_doctor_by_id(db: Session, doctor_id: str):
    """Fetch a doctor by their ID."""
    return db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()

def get_all_doctors(db: Session):
    """Fetch all doctors."""
    return db.query(Doctor).all()

def create_doctor(db: Session, doctor_data: DoctorCreate):
    """Create a new doctor."""
    new_doctor = Doctor(
        full_name=doctor_data.full_name,
        birth_date=doctor_data.birth_date,
        gender=doctor_data.gender,
        address=doctor_data.address,
        phone_number=doctor_data.phone_number,
        national_id=doctor_data.national_id,
        experience=doctor_data.experience,
        department_id=doctor_data.department_id,
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def update_doctor(db: Session, doctor_id: str, doctor_data: DoctorUpdate):
    """Update an existing doctor."""
    db_doctor = get_doctor_by_id(db, doctor_id)
    if not db_doctor:
        return None

    update_data = doctor_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_doctor, key, value)

    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: str):
    """Delete a doctor."""
    db_doctor = get_doctor_by_id(db, doctor_id)
    if not db_doctor:
        return None

    db.delete(db_doctor)
    db.commit()
    return db_doctor