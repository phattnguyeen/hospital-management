# Hospital Management Backend

This is the backend for the Hospital Management System. It is built using FastAPI and SQLAlchemy, and it connects to a PostgreSQL database.

## Requirements

- Python 3.9+
- PostgreSQL

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/PhatNguyen3174/hospital-management.git
   cd hospital-management-backend
   ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt

4. Running the Application
    ```sh 
    uvicorn main:app --reload
    ```
