from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("$2b$12$KL.VK8TsyPvMyGEm/KJZr.wJjbawpzNVDCw6QMTzvPI1j8dtGj5NW")
print(hashed_password)
print(pwd_context)  # Should look like: $2b$12$...
