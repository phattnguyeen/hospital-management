from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta
from database import SessionLocal
from models import Patient
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Patient Management API", description="API for managing patient records", version="1.0.0")

# Secret key to encode the JWT token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular Frontend
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Define a Pydantic model for request validation
class PatientCreate(BaseModel):
    username: str = Field(...)
    name: str = Field(...)
    age: int = Field(..., ge=0)
    password: str = Field(...)
    phone_no: str = Field(None)
    address: str = Field(None)
    patient_type: str = Field(None)
    sex: str = Field(None)
    admit_date: date = Field(None)
    discharge_date: date = Field(None)

class PatientUpdate(BaseModel):
    username: str = Field(None)
    name: str = Field(None)
    age: int = Field(None, ge=0)
    password: str = Field(None, min_length=6)
    phone_no: str = Field(None)
    address: str = Field(None)
    patient_type: str = Field(None)
    sex: str = Field(None)
    admit_date: date = Field(None)
    discharge_date: date = Field(None)

# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str


# Dependency: Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Utility function: Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Utility function: Hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# Utility function: Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Login route with OAuth2
@app.post("/login", response_model=Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Patient).filter(Patient.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Get the current logged-in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(Patient).filter(Patient.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Protected route example
# @app.get("/users/me", tags=["Users"])
# def read_users_me(current_user: Patient = Depends(get_current_user)):
#     return {"username": current_user.username, "name": current_user.name}

@app.post("/patients/", tags=["Patients"])
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(patient.password)
    new_patient = Patient(
        username=patient.username,
        name=patient.name,
        age=patient.age,
        password=hashed_password,
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
    
    if patient.username is not None:
        db_patient.username = patient.username
    if patient.name is not None:
        db_patient.name = patient.name
    if patient.age is not None:
        db_patient.age = patient.age
    if patient.password is not None:
        db_patient.password = get_password_hash(patient.password)
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