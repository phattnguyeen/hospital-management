CREATE SEQUENCE patient_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_patient_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.patient_id IS NULL THEN
        NEW.patient_id := 'PAT' || lpad(nextval('patient_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER patient_id_trigger
BEFORE INSERT ON patient
FOR EACH ROW
EXECUTE FUNCTION generate_patient_id();

-------------- TRIGGER FOR DOCTOR ----------------
CREATE SEQUENCE doctor_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_doctor_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.doctor_id IS NULL THEN
        NEW.doctor_id := 'DOC' || lpad(nextval('doctor_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER doctor_id_trigger
BEFORE INSERT ON doctor
FOR EACH ROW
EXECUTE FUNCTION generate_doctor_id();

---- Employee ---
CREATE SEQUENCE employee_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_employee_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.employee_id IS NULL THEN
        NEW.employee_id := 'EMP' || lpad(nextval('employee_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER employee_id_trigger
BEFORE INSERT ON employee
FOR EACH ROW
EXECUTE FUNCTION generate_employee_id();

---------- Invoice -----------

CREATE SEQUENCE invoice_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_invoice_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.invoice_id IS NULL THEN
        NEW.invoice_id := 'INV' || lpad(nextval('invoice_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER invoice_id_trigger
BEFORE INSERT ON invoice
FOR EACH ROW
EXECUTE FUNCTION generate_invoice_id();

---- Medical ---

CREATE SEQUENCE medicine_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_medicine_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.medicine_id IS NULL THEN
        NEW.medicine_id := 'MEC' || lpad(nextval('medicine_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER medicine_id_trigger
BEFORE INSERT ON medicine
FOR EACH ROW
EXECUTE FUNCTION generate_medicine_id();


-------- Appointment --------

CREATE SEQUENCE appointment_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_appointment_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.appointment_id IS NULL THEN
        NEW.appointment_id := 'APP' || lpad(nextval('appointment_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER appointment_id_trigger
BEFORE INSERT ON appointment
FOR EACH ROW
EXECUTE FUNCTION generate_appointment_id();


---- Medical Exam ----
CREATE SEQUENCE medical_examination_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE FUNCTION generate_medical_examination_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.exam_id IS NULL THEN
        NEW.exam_id := 'MEDEXAM' || lpad(nextval('medical_examination_seq')::text, 5, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER medical_examination_exam_trigger
BEFORE INSERT ON medical_examination
FOR EACH ROW
EXECUTE FUNCTION generate_medical_examination_id();
