from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

def get_department_by_id(db: Session, department_id: str):
    """Fetch a department by its ID."""
    return db.query(Department).filter(Department.department_id == department_id).first()

def get_all_departments(db: Session):
    """Fetch all departments."""
    return db.query(Department).all()

def create_department(db: Session, department_data: DepartmentCreate):
    """Create a new department."""
    new_department = Department(
        department_id= department_data.department_id,  # Use the explicitly passed department_id
        department_name=department_data.department_name
    )
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

def update_department(db: Session, department_id: str, department_data: DepartmentUpdate):
    """Update an existing department."""
    db_department = get_department_by_id(db, department_id)
    if not db_department:
        return None

    update_data = department_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_department, key, value)

    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: str):
    """Delete a department."""
    db_department = get_department_by_id(db, department_id)
    if not db_department:
        return None

    db.delete(db_department)
    db.commit()
    return db_department