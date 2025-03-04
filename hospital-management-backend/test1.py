from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("alex")
print(hashed_password)  # Should look like: $2b$12$...
