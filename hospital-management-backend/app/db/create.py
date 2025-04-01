from sqlalchemy import (
    create_engine, Column, String, Integer, Text, Date, ForeignKey, DECIMAL, Time, CheckConstraint, event
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
import random
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

DATABASE_URL = "postgresql://phatnguyen:fFqMCm0RqQwdwq0rujX4IyNpHcCg8DA2@dpg-cvameh5svqrc73bvpveg-a.oregon-postgres.render.com/hospitalmanagement_txr6"

# Initialize database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def generate_unique_id(session: Session, prefix: str, table: str, column: str):
    while True:
        new_id = f"{prefix}{random.randint(10000, 99999)}"
        if not session.execute(f"SELECT 1 FROM {table} WHERE {column} = :id", {"id": new_id}).fetchone():
            return new_id
# Department Table
class Department(Base):
    __tablename__ = "department"
    department_id = Column(String(20), primary_key=True)
    department_name = Column(String(100), nullable=False)

def before_insert_department(mapper, connection, target):
    session = SessionLocal()
    target.department_id = generate_unique_id(session, "DEP", "department", "department_id")
    session.close()

event.listen(Department, "before_insert", before_insert_department)
    


# Patient Table
class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(String(20), primary_key=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(20), unique=True)
    medical_history = Column(Text)

def before_insert_patient(mapper, connection, target):
    session = SessionLocal()
    target.patient_id = generate_unique_id(session, "PAT", "patient", "patient_id")
    session.close()

event.listen(Patient, "before_insert", before_insert_patient)

# Doctor Table
class Doctor(Base):
    __tablename__ = "doctor"
    doctor_id = Column(String(20), primary_key=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(20), unique=True)
    national_id = Column(String(20), unique=True)
    experience = Column(Integer, CheckConstraint("experience >= 0"))
    department_id = Column(String(20), ForeignKey("department.department_id"), nullable=True)

def before_insert_doctor(mapper, connection, target):
    session = SessionLocal()
    target.doctor_id = generate_unique_id(session, "DOC", "doctor", "doctor_id")
    session.close()

event.listen(Doctor, "before_insert", before_insert_doctor)
# Insurance Table
class Insurance(Base):
    __tablename__ = "insurance"
    insurance_id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patient.patient_id"), nullable=False)
    treatment_facility = Column(String(255))

# Room Table
class Room(Base):
    __tablename__ = "room"
    room_id = Column(String(20), primary_key=True)
    room_type = Column(String(50), nullable=False)
    bed_id = Column(String(50), nullable=False)
    status = Column(String(50))
    department_id = Column(String(20), ForeignKey("department.department_id"), nullable=True)

# Employee Table
class Employee(Base):
    __tablename__ = "employee"
    employee_id = Column(String(20), primary_key=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(20), unique=True)
    position = Column(String(50), nullable=False)
    department_id = Column(String(20), ForeignKey("department.department_id"), nullable=True)

def before_insert_employee(mapper, connection, target):
    session = SessionLocal()
    target.employee_id = generate_unique_id(session, "EMP", "employee", "employee_id")
    session.close()

event.listen(Employee, "before_insert", before_insert_employee)

class Account(Base):
    __tablename__ = 'account'
    account_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    username = Column(String(50), unique=True, nullable=False)
    passwordHash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    patient_id = Column(String(20), ForeignKey('patient.patient_id', ondelete='CASCADE'), unique=True)
    doctor_id = Column(String(20), ForeignKey('doctor.doctor_id', ondelete='CASCADE'), unique=True)
    employee_id = Column(String(20), ForeignKey('employee.employee_id', ondelete='CASCADE'), unique=True)

# Invoice Table
class Invoice(Base):
    __tablename__ = "invoice"
    invoice_id = Column(String(20), primary_key=True)
    total_amount = Column(DECIMAL(15, 2), CheckConstraint("total_amount >= 0"))
    expense = Column(DECIMAL(15, 2), CheckConstraint("expense >= 0"))
    payment_date = Column(Date)
    status = Column(String(50))
    employee_id = Column(String(20), ForeignKey("employee.employee_id"), nullable=True)

def before_insert_invoice(mapper, connection, target):
    session = SessionLocal()
    target.invoice_id = generate_unique_id(session, "INV", "invoice", "invoice_id")
    session.close()

event.listen(Invoice, "before_insert", before_insert_invoice)

# Medicine Table
class Medicine(Base):
    __tablename__ = "medicine"
    medicine_id = Column(String(20), primary_key=True)
    medicine_name = Column(String(100), nullable=False)
    category = Column(String(50))
    unit = Column(String(20))
    price = Column(DECIMAL(10, 2), CheckConstraint("price >= 0"))
    expiration_date = Column(Date)
    notes = Column(Text)

def before_insert_medicine(mapper, connection, target):
    session = SessionLocal()
    target.medicine_id = generate_unique_id(session, "MED", "medicine", "medicine_id")
    session.close()

event.listen(Medicine, "before_insert", before_insert_medicine)

# Service Table
class Service(Base):
    __tablename__ = "service"
    service_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    service_name = Column(String(100), nullable=False)
    unit_price = Column(DECIMAL(10, 2), CheckConstraint("unit_price >= 0"))
    unit = Column(String(20))

# Prescription Table
class Prescription(Base):
    __tablename__ = "prescription"
    medicine_id = Column(String(20), ForeignKey("medicine.medicine_id"), primary_key=True)
    doctor_id = Column(String(20), ForeignKey("doctor.doctor_id"), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patient.patient_id"), primary_key=True)
    invoice_id = Column(String(20), ForeignKey("invoice.invoice_id"), nullable=True)
    quantity = Column(Integer, CheckConstraint("quantity > 0"))
    prescription_date = Column(Date)
    notes = Column(Text)

# Appointment Table
class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = Column(String(20), ForeignKey("doctor.doctor_id"), nullable=False)
    request_date = Column(Date, nullable=False)
    appointment_time = Column(Time)
    status = Column(String(50))
    appointment_date = Column(Date, nullable=False)

def before_insert_appointmentt(mapper, connection, target):
    session = SessionLocal()
    target.medicine_id = generate_unique_id(session, "APP", "appointment", "appointment_id")
    session.close()

event.listen(Appointment, "before_insert", before_insert_appointmentt)   

# Medical Examination Table
class MedicalExamination(Base):
    __tablename__ = "medical_examination"
    exam_id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = Column(String(20), ForeignKey("doctor.doctor_id"), nullable=False)
    exam_date = Column(Date, nullable=False)
    symptoms = Column(Text)
    disease_id = Column(UUID(as_uuid=True), ForeignKey("disease.disease_id"), nullable=True)

def before_insert_medicalexam(mapper, connection, target):
    session = SessionLocal()
    target.exam_id = generate_unique_id(session, "MEDEXAM", "medical_examination", "exam_id")
    session.close()

event.listen(MedicalExamination, "before_insert", before_insert_medicalexam)   


# Disease Table
class Disease(Base):
    __tablename__ = "disease"
    disease_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    disease_name = Column(String(100), nullable=False)

# Medical Record Table
class MedicalRecord(Base):
    __tablename__ = "medical_record"
    record_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    patient_id = Column(String(20), ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = Column(String(20), ForeignKey("doctor.doctor_id"), nullable=False)
    exam_date = Column(Date, nullable=False)
    symptoms = Column(Text)
    diagnosis = Column(Text)
    treatment = Column(Text)
    department_id = Column(String(20), ForeignKey("department.department_id"), nullable=True)

# Service Detail Table
class ServiceDetail(Base):
    __tablename__ = "service_detail"
    service_id = Column(UUID(as_uuid=True), ForeignKey("service.service_id"), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patient.patient_id"), primary_key=True)
    quantity = Column(Integer, CheckConstraint("quantity > 0"))
    usage_date = Column(Date, nullable=False)

# Function to create tables
def create_tables():
    """Ensure tables are created in the database."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

# Drop tables in the database
def drop_tables():
    """Drop all tables in the database."""
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully!")

if __name__ == "__main__":

    drop_tables()
