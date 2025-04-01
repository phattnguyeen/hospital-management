from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("123")
print(hashed_password)
print(pwd_context)  # Should look like: $2b$12$...
