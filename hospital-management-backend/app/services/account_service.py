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

def get_account_by_phone_number(db: Session, phone_number: str):
    """Fetch an account by its phone number."""
    return db.query(Account).filter(Account.phone_number == phone_number).first()

def create_account(db: Session, account_data: AccountCreate):
    """Create a new account with a default password."""
    # Check if the phone number is already in use
    existing_account = get_account_by_phone_number(db, account_data.phone_number)
    if existing_account:
        raise ValueError("Phone number is already in use.")

    # Hash the default password
    default_password = "123"
    hashed_password = get_password_hash(default_password)

    new_account = Account(
        password_hash=hashed_password,
        phone_number=account_data.phone_number,
        is_verified=True
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

    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

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
