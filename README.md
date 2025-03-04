# Hospital Website

This project is a web application for managing hospital operations, including patient records, appointments, and staff management.

## Features

- Patient registration and management
- Appointment scheduling
- Staff management
- Medical records management
- Billing and payments

## Technologies Used

- Angular (Frontend)
- Python (Backend)
- HTML
- CSS
- JavaScript
- Node.js
- Express.js
- PostgreSQL (Database)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/PhatNguyen3174/hospital-management.git
    ```
2. Navigate to the project directory:
    ```bash
    cd hospital-web
    ```
3. Install the dependencies for the frontend:
    ```bash
    cd hospital-management-frontend
    npm install
    ```
4. Install the dependencies for the backend:
    ```bash
    cd hospital-management-backend
    pip install -r requirements.txt
    ```

## Setting Up the Database

1. Ensure PostgreSQL is installed and running on your machine.
2. Create a new PostgreSQL database:
    ```bash
    createdb hospital_management
    ```
3. Run the SQL script to set up the database schema and initial data:
    ```bash
    psql -d hospital_management -f database/hostpital_data.sql
    ```

## Running the Application

1. Start the backend server:
    ```bash
    cd hospital-management-backend
    python app.py
    ```
2. Start the frontend server:
    ```bash
    cd hospital-management-frontend
    ng serve
    ```
3. Open your web browser and go to `http://localhost:4200`

## Contributing

Contributions are welcome! Please read the contributing guidelines first.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries, please contact us at [phatnguyen9712@gmail.com](mailto:phatnguyen9712@gmail.com).

## References

- Khan, R.S. and Saber, M., 2010. Design of a hospital-based database system (A case study of BIRDEM). International Journal on Computer Science and Engineering (IJCSE), 2(08), pp.2616-2621.
- Usoh, M.A., Udoiwod, E.N. and Chinemenma, I.S., 2022. Development of a Hospital Management Software for a Primary Healthcare Centre. Development, 9(9).
- [Hoan My Hospital](https://hoanmy.com/en/)
- [Hospital / Health Care center 3D WalkThrough Animation by Frame Channel](https://www.youtube.com/watch?v=e89J3eW4a24)
