from app.db.database import engine, Base
from app.models.patient import Patient

# Create all tables in the database
Base.metadata.create_all(bind=engine)
print("Tables created successfully")