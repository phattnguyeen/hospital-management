from sqlalchemy import create_engine, text

# Define the DATABASE_URL
DATABASE_URL = "postgresql://postgres:Phat121002%40@localhost:5433/hospital_management"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Connect to the database
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM patient;"))
        for row in result:
            print(row)
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")