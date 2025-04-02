from sqlalchemy.orm import Session
from app.models.insurance import Insurance
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate

def get_insurance_by_id(db: Session, insurance_id: str):
    """Fetch an insurance record by its ID."""
    return db.query(Insurance).filter(Insurance.insurance_id == insurance_id).first()

def get_all_insurances(db: Session):
    """Fetch all insurance records."""
    return db.query(Insurance).all()

def create_insurance(db: Session, insurance_data: InsuranceCreate):
    """Create a new insurance record."""
    new_insurance = Insurance(
        isurance_id=insurance_data.insurance_id,
        patient_id=insurance_data.patient_id,
        treatment_facility=insurance_data.treatment_facility,
    )
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)
    return new_insurance

def update_insurance(db: Session, insurance_id: str, insurance_data: InsuranceUpdate):
    """Update an existing insurance record."""
    db_insurance = get_insurance_by_id(db, insurance_id)
    if not db_insurance:
        return None

    update_data = insurance_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_insurance, key, value)

    db.commit()
    db.refresh(db_insurance)
    return db_insurance

def delete_insurance(db: Session, insurance_id: str):
    """Delete an insurance record."""
    db_insurance = get_insurance_by_id(db, insurance_id)
    if not db_insurance:
        return None

    db.delete(db_insurance)
    db.commit()
    return db_insurance