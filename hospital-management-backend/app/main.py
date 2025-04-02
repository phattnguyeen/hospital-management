from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from uuid import UUID
import jwt

from app.db.database import get_db
from app.services import patient_service, account_service, department_service, doctor_service
from app.services import employee_service, insurance_service
from app.schemas.account import AccountCreate, AccountUpdate
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.schemas.patient import PatientCreate, PatientUpdate
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.auth import Token
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidTokenError

# FastAPI app
app = FastAPI(title="Hospital Management API", description="API for hospital management", version="1.0.0")

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

    user = account_service.get_account_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/login", response_model=Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access token.
    """
    user = account_service.get_account_by_username(db, form_data.username)
    if not user or not account_service.verify_password(form_data.password, user.passwordHash):  # Use passwordHash
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



@app.post("/accounts/", tags=["Accounts"])
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """Create a new account."""
    new_account = account_service.create_account(db, account)
    return {"message": "Account created successfully", "account_id": new_account.account_id}


@app.get("/accounts/{account_id}", tags=["Accounts"])
def read_account(account_id: UUID, db: Session = Depends(get_db)):
    """Fetch an account by ID."""
    account = account_service.get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.put("/accounts/{account_id}", tags=["Accounts"])
def update_account(account_id: UUID, account: AccountUpdate, db: Session = Depends(get_db)):
    """Update an account."""
    updated_account = account_service.update_account(db, account_id, account)
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully", "account_id": updated_account.account_id}


@app.delete("/accounts/{account_id}", tags=["Accounts"])
def delete_account(account_id: UUID, db: Session = Depends(get_db)):
    """Delete an account."""
    deleted_account = account_service.delete_account(db, account_id)
    if not deleted_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}


@app.post("/patients/", tags=["Patients"])
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient record."""
    new_patient = patient_service.create_patient(db, patient)
    return {"message": "Patient created successfully", "patient_id": new_patient.patient_id}


@app.get("/patients/{patient_id}", tags=["Patients"])
def read_patient(patient_id: str, db: Session = Depends(get_db)):
    """Fetch a patient record by ID."""
    patient = patient_service.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.put("/patients/{patient_id}", tags=["Patients"])
def update_patient(patient_id: str, patient: PatientUpdate, db: Session = Depends(get_db)):
    """Update a patient record."""
    updated_patient = patient_service.update_patient(db, patient_id, patient)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient updated successfully", "patient_id": updated_patient.patient_id}


@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    """Delete a patient record."""
    deleted_patient = patient_service.delete_patient(db, patient_id)
    if not deleted_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}



@app.post("/departments/", tags=["Departments"])
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new account."""
    new_department = department_service.create_department(db, department)
    return {"message": "Deparment created successfully", "department_id": new_department.department_id}

@app.put("/departments/{department_id}", tags=["Departments"])
def update_department(department_id: str, department: DepartmentUpdate, db: Session = Depends(get_db)):
    """
    Update an existing department record.
    """
    updated_department = department_service.update_department(db, department_id, department)
    if not updated_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department updated successfully", "department_id": updated_department.department_id}


@app.delete("/departments/{department_id}", tags=["Departments"])
def delete_department(department_id: str, db: Session = Depends(get_db)):
    """
    Delete a department record.
    """
    deleted_department = department_service.delete_department(db, department_id)
    if not deleted_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department deleted successfully"}

@app.get("/departments/", tags=["Departments"])
def get_all_departments(db: Session = Depends(get_db)):
    """
    Fetch all departments.
    """
    departments = department_service.get_all_departments(db)
    return departments



# Doctor Endpoints
@app.post("/doctors/", tags=["Doctors"])
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """Create a new doctor record."""
    new_doctor = doctor_service.create_doctor(db, doctor)
    return {"message": "Doctor created successfully", "doctor_id": new_doctor.doctor_id}

@app.get("/doctors/{doctor_id}", tags=["Doctors"])
def read_doctor(doctor_id: str, db: Session = Depends(get_db)):
    """Fetch a doctor record by ID."""
    doctor = doctor_service.get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.put("/doctors/{doctor_id}", tags=["Doctors"])
def update_doctor(doctor_id: str, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    """Update a doctor record."""
    updated_doctor = doctor_service.update_doctor(db, doctor_id, doctor)
    if not updated_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor updated successfully", "doctor_id": updated_doctor.doctor_id}

@app.delete("/doctors/{doctor_id}", tags=["Doctors"])
def delete_doctor(doctor_id: str, db: Session = Depends(get_db)):
    """Delete a doctor record."""
    deleted_doctor = doctor_service.delete_doctor(db, doctor_id)
    if not deleted_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}

@app.get("/doctors/", tags=["Doctors"])
def get_all_doctors(db: Session = Depends(get_db)):
    """Fetch all doctors."""
    doctors = doctor_service.get_all_doctors(db)
    return doctors


# Employee Endpoints
@app.post("/employees/", tags=["Employees"])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee record."""
    new_employee = employee_service.create_employee(db, employee)
    return {"message": "Employee created successfully", "employee_id": new_employee.employee_id}

@app.get("/employees/{employee_id}", tags=["Employees"])
def read_employee(employee_id: str, db: Session = Depends(get_db)):
    """Fetch an employee record by ID."""
    employee = employee_service.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", tags=["Employees"])
def update_employee(employee_id: str, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    """Update an employee record."""
    updated_employee = employee_service.update_employee(db, employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully", "employee_id": updated_employee.employee_id}

@app.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    """Delete an employee record."""
    deleted_employee = employee_service.delete_employee(db, employee_id)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

@app.get("/employees/", tags=["Employees"])
def get_all_employees(db: Session = Depends(get_db)):
    """Fetch all employees."""
    employees = employee_service.get_all_employees(db)
    return employees

# Insurance Endpoints
@app.post("/insurances/", tags=["Insurances"])
def create_insurance(insurance: InsuranceCreate, db: Session = Depends(get_db)):
    """Create a new insurance record."""
    new_insurance = insurance_service.create_insurance(db, insurance)
    return {"message": "Insurance created successfully", "insurance_id": new_insurance.insurance_id}

@app.get("/insurances/{insurance_id}", tags=["Insurances"])
def read_insurance(insurance_id: str, db: Session = Depends(get_db)):
    """Fetch an insurance record by ID."""
    insurance = insurance_service.get_insurance_by_id(db, insurance_id)
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance

@app.put("/insurances/{insurance_id}", tags=["Insurances"])
def update_insurance(insurance_id: str, insurance: InsuranceUpdate, db: Session = Depends(get_db)):
    """Update an insurance record."""
    updated_insurance = insurance_service.update_insurance(db, insurance_id, insurance)
    if not updated_insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return {"message": "Insurance updated successfully", "insurance_id": updated_insurance.insurance_id}

@app.delete("/insurances/{insurance_id}", tags=["Insurances"])
def delete_insurance(insurance_id: str, db: Session = Depends(get_db)):
    """Delete an insurance record."""
    deleted_insurance = insurance_service.delete_insurance(db, insurance_id)
    if not deleted_insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return {"message": "Insurance deleted successfully"}

@app.get("/insurances/", tags=["Insurances"])
def get_all_insurances(db: Session = Depends(get_db)):
    """Fetch all insurance records."""
    insurances = insurance_service.get_all_insurances(db)
    return insurances