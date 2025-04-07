from sqlalchemy import create_engine, text

# Define the DATABASE_URL
DATABASE_URL = "postgresql://hmsdb_owner:npg_9IzgxcpTou6D@ep-proud-snowflake-a5e4oyfd-pooler.us-east-2.aws.neon.tech/hmsdb?sslmode=require"

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