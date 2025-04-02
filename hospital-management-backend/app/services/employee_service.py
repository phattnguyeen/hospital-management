from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

def get_employee_by_id(db: Session, employee_id: str):
    """Fetch an employee by their ID."""
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()

def get_all_employees(db: Session):
    """Fetch all employees."""
    return db.query(Employee).all()

def create_employee(db: Session, employee_data: EmployeeCreate):
    """Create a new employee."""
    new_employee = Employee(
        full_name=employee_data.full_name,
        birth_date=employee_data.birth_date,
        gender=employee_data.gender,
        address=employee_data.address,
        phone_number=employee_data.phone_number,
        position=employee_data.position,
        department_id=employee_data.department_id,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

def update_employee(db: Session, employee_id: str, employee_data: EmployeeUpdate):
    """Update an existing employee."""
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        return None

    update_data = employee_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: str):
    """Delete an employee."""
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        return None

    db.delete(db_employee)
    db.commit()
    return db_employee