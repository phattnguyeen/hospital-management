from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import date
from database import SessionLocal
from models import Patient
from uuid import UUID

app = FastAPI(title="Patient Management API", description="API for managing patient records", version="1.0.0")

# Define a Pydantic model for request validation
class PatientCreate(BaseModel):
    name: str = Field(...)
    age: int = Field(..., ge=0)
    password: str = Field(..., min_length=6)
    phone_no: str = Field(None)
    address: str = Field(None)
    patient_type: str = Field(None)
    sex: str = Field(None)
    admit_date: date = Field(None)
    discharge_date: date = Field(None)

class PatientUpdate(BaseModel):
    name: str = Field(None)
    age: int = Field(None, ge=0)
    password: str = Field(None, min_length=6)
    phone_no: str = Field(None)
    address: str = Field(None)
    patient_type: str = Field(None)
    sex: str = Field(None)
    admit_date: date = Field(None)
    discharge_date: date = Field(None)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients/", tags=["Patients"])
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        password=patient.password,
        phone_no=patient.phone_no,
        address=patient.address,
        patient_type=patient.patient_type,
        sex=patient.sex,
        admit_date=patient.admit_date,
        discharge_date=patient.discharge_date
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "Patient created successfully", "patient_id": new_patient.patient_id}

@app.put("/patients/{patient_id}", tags=["Patients"])
def update_patient(patient_id: UUID, patient: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if patient.name is not None:
        db_patient.name = patient.name
    if patient.age is not None:
        db_patient.age = patient.age
    if patient.password is not None:
        db_patient.password = patient.password
    if patient.phone_no is not None:
        db_patient.phone_no = patient.phone_no
    if patient.address is not None:
        db_patient.address = patient.address
    if patient.patient_type is not None:
        db_patient.patient_type = patient.patient_type
    if patient.sex is not None:
        db_patient.sex = patient.sex
    if patient.admit_date is not None:
        db_patient.admit_date = patient.admit_date
    if patient.discharge_date is not None:
        db_patient.discharge_date = patient.discharge_date
    
    db.commit()
    db.refresh(db_patient)
    return {"message": "Patient updated successfully", "patient_id": db_patient.patient_id}

@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: UUID, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}