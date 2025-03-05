# Hospital Management Backend

This is the backend for the Hospital Management System. It is built using FastAPI and SQLAlchemy, and it connects to a PostgreSQL database.

## Requirements

- Python 3.9+
- PostgreSQL

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/PhatNguyen3174/hospital-management.git
   cd hospital-management-backend
   ```

2. **Create a virtual environment and activate it**:

   ```sh
   python -m venv venv
   source venv/Scripts/activate  # Windows
   source venv/bin/activate      # macOS/Linux
   ```

3. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. **Set up environment variables**:
   
   Create a `.env` file in the root directory and add the following:
   
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/hospital_db
   SECRET_KEY=your_secret_key
   ```

2. **Apply database migrations**:

   ```sh
   alembic upgrade head
   ```

3. **Start the FastAPI server**:

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

The application will be accessible at: [http://localhost:8000](http://localhost:8000)

## API Documentation

FastAPI provides automatic API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
hospital-management-backend/
│── app/
│   │── core/
│   │   │── config.py       # Configuration settings
│   │   │── security.py     # Security utilities (authentication, OAuth2, etc.)
│   │── schemas/
│   │   │── user.py         # Pydantic models for request/response
│   │   │── hospital.py     # Pydantic models for hospital entities
│   │── services/
│   │   │── user_service.py # Business logic for user handling
│   │   │── hospital_service.py # Business logic for hospitals
│   │── models/
│   │   │── user.py         # SQLAlchemy models for users
│   │   │── hospital.py     # SQLAlchemy models for hospitals
│   │── api/
│   │   │── v1/
│   │   │   │── endpoints/
│   │   │   │   │── user.py  # Routes related to users
│   │   │   │   │── hospital.py  # Routes related to hospitals
│   │   │   │── api_v1.py   # Include all versioned routes
│   │── db/
│   │   │── database.py     # Database connection setup
│   │   │── base.py         # Base SQLAlchemy model class
│   │── main.py            # FastAPI entry point
│── migrations/            # Alembic migration scripts
│── tests/                 # Test cases
│── .env                   # Environment variables
│── requirements.txt       # Dependencies
│── README.md              # Documentation

```

## Running Tests

To run tests, use:

```sh
pytest
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

---

For any issues or feature requests, please create an issue on GitHub.

