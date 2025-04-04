import pyotp
from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate
from uuid import UUID
from passlib.context import CryptContext
from twilio.rest import Client  # type: ignore
import random


from dotenv import load_dotenv
import os
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv(".env")  # Load environment variables from .env file

# # Twilio credentials (replace with your actual credentials)
# TWILIO_ACCOUNT_SID = 'AC09bf04efa93ae42365980b3b2361d2df'
# TWILIO_AUTH_TOKEN = '0315a992197dd70559d1e8b15a560ab1'
# TWILIO_PHONE_NUMBER = '+12318880770'  # Replace with your verified Twilio phone number

#Twilio credentials loaded from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a plain password matches a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_otp() -> str:
    """Generates a 6-digit OTP."""
    return f"{random.randint(100000, 999999)}"

def send_otp(phone_number: str, otp: str):
    """Send OTP to user's phone via SMS using Twilio."""
    try:
        print(f"Sending OTP to: {phone_number}")  # Debugging step
        message = client.messages.create(
            body=f"Your OTP is: {otp}. It is valid for 5 minutes.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"OTP sent successfully. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        raise RuntimeError(f"Failed to send OTP: {e}")


def verify_otp(user_otp: str, generated_otp: str) -> bool:
    """Verifies if the provided OTP matches the generated OTP."""
    return user_otp == generated_otp

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
    """Create a new account with OTP verification via SMS."""
     # Check if the phone number is already in use
    existing_account = get_account_by_phone_number(db, account_data.phone_number)
    if existing_account:
        raise ValueError("Phone number is already in use.")

    # Validate the role
    # valid_roles = ["patient", "doctor", "employee", "admin"]
    # if account_data.role not in valid_roles:
    #     raise ValueError(f"Invalid role. Allowed roles are: {', '.join(valid_roles)}")

    # Generate and send OTP
    otp = generate_otp()
    send_otp(account_data.phone_number, otp)

    # Simulate OTP verification (this should be handled by the front-end)
    user_otp = input("Enter the OTP you received: ")
    if user_otp != otp:
        raise ValueError("Invalid OTP entered.")

    # Hash the password and create the account
    hashed_password = get_password_hash(account_data.password)
    new_account = Account(
        password_hash=hashed_password,
        # role=account_data.role,
        phone_number=account_data.phone_number,
        is_verified=True,  # Set to True after successful OTP verification
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def update_account(db: Session, account_id: UUID, account_data: AccountUpdate):
    """Update an existing account and send OTP if phone number is updated."""
    db_account = get_account_by_id(db, account_id)
    if not db_account:
        return None

    update_data = account_data.dict(exclude_unset=True)

    # Hash the password if it's being updated
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    # Check if phone number is being updated
    if "phone_number" in update_data and update_data["phone_number"] != db_account.phone_number:
        otp = generate_otp()
        send_otp(update_data["phone_number"], otp)

        # Simulate OTP verification (this should be handled by the front-end)
        user_otp = input("Enter the OTP you received: ")

        # Verify the OTP
        if not verify_otp(user_otp, otp):
            raise ValueError("Invalid OTP entered.")

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