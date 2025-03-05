CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password TEXT NOT NULL,
    age INT CHECK (age >= 0),
    phone_no VARCHAR(15) UNIQUE,
    address TEXT,
    patient_type VARCHAR(50),
    sex VARCHAR(10) CHECK (sex IN ('Male', 'Female', 'Other')),
    admit_date DATE,
    discharge_date DATE,
    CHECK (discharge_date IS NULL OR discharge_date >= admit_date)
);


INSERT INTO patient (name, password, age, phone_no, address, patient_type, sex, admit_date, discharge_date)
VALUES
    ('John Doe', 'hashed_password1', 35, '1234567890', '123 Main St, NY', 'Inpatient', 'Male', '2024-02-20', '2024-03-01'),
    ('Jane Smith', 'hashed_password2', 29, '0987654321', '456 Oak St, CA', 'Outpatient', 'Female', '2024-02-25', NULL),
    ('Alex Johnson', 'hashed_password3', 42, '1122334455', '789 Pine St, TX', 'Inpatient', 'Other', '2024-01-15', '2024-02-10'),
    ('Emily Brown', 'hashed_password4', 31, '6677889900', '321 Elm St, FL', 'Outpatient', 'Female', '2024-02-28', NULL),
    ('Michael Lee', 'hashed_password5', 50, '5544332211', '654 Cedar St, WA', 'Inpatient', 'Male', '2024-01-10', '2024-01-20');

select * from patient