from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate
from uuid import UUID
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a plain password matches a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_account_by_id(db: Session, account_id: UUID):
    """Fetch an account by its ID."""
    return db.query(Account).filter(Account.account_id == account_id).first()

def get_account_by_username(db: Session, username: str):
    """Fetch an account by its username."""
    return db.query(Account).filter(Account.username == username).first()

def create_account(db: Session, account_data: AccountCreate):
    """Create a new account."""
    hashed_password = get_password_hash(account_data.password)  # Hash the password
    new_account = Account(
        username=account_data.username,
        passwordHash=hashed_password,  # Save the hashed password
        role=account_data.role,
        user_id=account_data.user_id,
        user_type=account_data.user_type,
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def update_account(db: Session, account_id: UUID, account_data: AccountUpdate):
    """Update an existing account."""
    db_account = get_account_by_id(db, account_id)
    if not db_account:
        return None

    update_data = account_data.dict(exclude_unset=True)

    # Hash the password if it's being updated
    if "password" in update_data:
        update_data["passwordHash"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_account, key, value)

    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: UUID):
    """Delete an account."""
    db_account = get_account_by_id(db, account_id)
    if not db_account:
        return None

    db.delete(db_account)
    db.commit()
    return db_account