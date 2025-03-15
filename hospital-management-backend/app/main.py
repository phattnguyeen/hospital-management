# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from uuid import UUID
import jwt

from app.db.database import get_db
from app.services import patient_service
from app.schemas.patient import PatientCreate, PatientUpdate
from app.schemas.auth import Token
from app.models.patient import Patient
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidTokenError

# FastAPI app
app = FastAPI(title="Patient Management API", description="API for managing patient records", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

# JWT settings
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Fetch the currently logged-in user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = patient_service.get_patient_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/login", response_model=Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access token.
    """
    user = patient_service.get_patient_by_username(db, form_data.username)
    if not user or not patient_service.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout", tags=["Auth"])
def logout():
    """
    Logout user by invalidating the JWT token.
    """
    return {"message": "Logout successful"}

@app.post("/patients/", tags=["Patients"])
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient record."""
    new_patient = patient_service.create_patient(db, patient)
    return {"message": "Patient created successfully", "patient_id": new_patient.patient_id}

@app.get("/patients/{patient_id}", tags=["Patients"])
def read_patient(patient_id: UUID, db: Session = Depends(get_db)):
    """Fetch a patient record by ID."""
    patient = patient_service.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", tags=["Patients"])
def update_patient(patient_id: UUID, patient: PatientUpdate, db: Session = Depends(get_db)):
    """Update a patient record."""
    updated_patient = patient_service.update_patient(db, patient_id, patient)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient updated successfully", "patient_id": updated_patient.patient_id}

@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: UUID, db: Session = Depends(get_db)):
    """Delete a patient record."""
    deleted_patient = patient_service.delete_patient(db, patient_id)
    if not deleted_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}