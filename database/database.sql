--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: hmsdb_owner 
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO hmsdb_owner ;

--
-- Name: check_duplicate_data(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.check_duplicate_data() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Kiểm tra trùng lặp national_id
    IF EXISTS (SELECT 1 FROM doctor WHERE national_id = NEW.national_id) OR
       EXISTS (SELECT 1 FROM employee WHERE national_id = NEW.national_id) OR
       EXISTS (SELECT 1 FROM patient WHERE national_id = NEW.national_id) THEN
        RAISE EXCEPTION 'Duplicate national_id: %', NEW.national_id;
    END IF;
    
    -- Kiểm tra trùng lặp phone_number
    IF EXISTS (SELECT 1 FROM doctor WHERE phone_number = NEW.phone_number) OR
       EXISTS (SELECT 1 FROM employee WHERE phone_number = NEW.phone_number) OR
       EXISTS (SELECT 1 FROM patient WHERE phone_number = NEW.phone_number) THEN
        RAISE EXCEPTION 'Duplicate phone_number: %', NEW.phone_number;
    END IF;
    
    -- Kiểm tra trùng lặp email
    IF EXISTS (SELECT 1 FROM doctor WHERE email = NEW.email) OR
       EXISTS (SELECT 1 FROM employee WHERE email = NEW.email) OR
       EXISTS (SELECT 1 FROM patient WHERE email = NEW.email) THEN
        RAISE EXCEPTION 'Duplicate email: %', NEW.email;
    END IF;

    -- Nếu không có trùng lặp, cho phép INSERT
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.check_duplicate_data() OWNER TO hmsdb_owner ;

--
-- Name: generate_appointment_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_appointment_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.appointment_id IS NULL THEN
        NEW.appointment_id := generate_unique_8digit_id('appointment', 'appointment_id');
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_appointment_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_dept_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_dept_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    prefix TEXT;
BEGIN
    -- Lấy ký tự đầu của từng từ trong dep_name
    prefix := UPPER(LEFT(NEW.department_name, 1));
    
    FOR i IN 2..LENGTH(NEW.department_name) LOOP
        IF SUBSTRING(NEW.department_name FROM i-1 FOR 1) = ' ' THEN
            prefix := prefix || UPPER(SUBSTRING(NEW.department_name FROM i FOR 1));
        END IF;
    END LOOP;

    -- Gán dept_id không có số thứ tự
    NEW.department_id := prefix;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_dept_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_doctor_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_doctor_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    random_number TEXT;
BEGIN
    -- Tạo số ngẫu nhiên gồm 4 chữ số
    random_number := LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
    
    -- Kiểm tra tính duy nhất của số ngẫu nhiên
    WHILE EXISTS (SELECT 1 FROM doctor WHERE doctor_id = NEW.department_id || random_number) LOOP
        -- Tạo lại số ngẫu nhiên nếu đã tồn tại
        random_number := LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
    END LOOP;
    
    -- Cập nhật doctor_id với department_id và số ngẫu nhiên
    NEW.doctor_id := NEW.department_id || random_number;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_doctor_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_employee_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_employee_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.employee_id IS NULL THEN
        NEW.employee_id := '3001' || lpad(nextval('employee_seq')::text, 4, '2');
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_employee_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_invoice_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_invoice_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.invoice_id IS NULL THEN
        NEW.invoice_id := generate_unique_8digit_id('invoice', 'invoice_id');
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_invoice_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_medical_examination_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_medical_examination_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.exam_id IS NULL THEN
        NEW.exam_id := generate_unique_8digit_id('medical_examination', 'exam_id');
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_medical_examination_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_medicine_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_medicine_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.medicine_id IS NULL THEN
        NEW.medicine_id := generate_unique_8digit_id('medicine', 'medicine_id');
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_medicine_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_patient_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_patient_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.patient_id := 'PAT-' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || '-' || NEXTVAL('patient_id_seq');
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_patient_id() OWNER TO hmsdb_owner ;

--
-- Name: generate_unique_8digit_id(text, text); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.generate_unique_8digit_id(table_name text, column_name text) RETURNS text
    LANGUAGE plpgsql
    AS $_$
DECLARE
    new_id TEXT;
    id_exists BOOLEAN;
BEGIN
    LOOP
        new_id := LPAD(FLOOR(RANDOM() * 100000000)::TEXT, 8, '0'); -- Tạo số ngẫu nhiên 8 chữ số
        -- Kiểm tra xem ID có tồn tại trong bảng hiện tại không
        EXECUTE FORMAT('SELECT EXISTS (SELECT 1 FROM %I WHERE %I = $1)', table_name, column_name)
        INTO id_exists USING new_id;

        IF NOT id_exists THEN
            EXIT;
        END IF;
    END LOOP;
    
    RETURN new_id;
END;
$_$;


ALTER FUNCTION public.generate_unique_8digit_id(table_name text, column_name text) OWNER TO hmsdb_owner ;

--
-- Name: update_account_role(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.update_account_role() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Kiểm tra xem số điện thoại có tồn tại trong bảng doctor không
    IF NEW.phone_number IS NOT NULL AND EXISTS (SELECT 1 FROM doctor WHERE phone_number = NEW.phone_number) THEN
        -- Nếu có, cập nhật role là 'doctor' trong bảng account
        UPDATE account
        SET role = 'doctor'
        WHERE phone_number = NEW.phone_number;
    
    -- Kiểm tra xem số điện thoại có tồn tại trong bảng employee không
    ELSIF NEW.phone_number IS NOT NULL AND EXISTS (SELECT 1 FROM employee WHERE phone_number = NEW.phone_number) THEN
        -- Nếu có, cập nhật role là 'employee' trong bảng account
        UPDATE account
        SET role = 'employee'
        WHERE phone_number = NEW.phone_number;
    
    -- Kiểm tra xem số điện thoại có tồn tại trong bảng patient không
    ELSIF NEW.phone_number IS NOT NULL AND EXISTS (SELECT 1 FROM patient WHERE phone_number = NEW.phone_number) THEN
        -- Nếu có, cập nhật role là 'patient' trong bảng account
        UPDATE account
        SET role = 'patient'
        WHERE phone_number = NEW.phone_number;

    -- Nếu không có số điện thoại (NULL), cập nhật role là 'admin' trong bảng account
    ELSIF NEW.phone_number IS NULL THEN
        UPDATE account
        SET role = 'admin'
        WHERE phone_number IS NULL;
    
    -- Nếu không có số điện thoại trong bất kỳ bảng nào, gán role là NULL trong bảng account
    ELSE
        UPDATE account
        SET role = NULL
        WHERE phone_number = NEW.phone_number;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_account_role() OWNER TO hmsdb_owner ;

--
-- Name: update_account_user_id(); Type: FUNCTION; Schema: public; Owner: hmsdb_owner 
--

CREATE FUNCTION public.update_account_user_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Kiểm tra và cập nhật user_id từ các bảng khác nhau
    IF TG_TABLE_NAME = 'doctor' THEN
        UPDATE account
        SET user_id = NEW.doctor_id  -- Sử dụng doctor_id nếu là bảng doctor
        WHERE phone_number = NEW.phone_number;
    ELSIF TG_TABLE_NAME = 'patient' THEN
        UPDATE account
        SET user_id = NEW.patient_id  -- Sử dụng patient_id nếu là bảng patient
        WHERE phone_number = NEW.phone_number;
    ELSIF TG_TABLE_NAME = 'employee' THEN
        UPDATE account
        SET user_id = NEW.employee_id  -- Sử dụng employee_id nếu là bảng employee
        WHERE phone_number = NEW.phone_number;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_account_user_id() OWNER TO hmsdb_owner ;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.account (
    account_id uuid DEFAULT gen_random_uuid() NOT NULL,
    password_hash character varying(255) NOT NULL,
    otp character varying(6),
    role character varying(50),
    user_id character varying(100),
    phone_number character varying(20) NOT NULL,
    is_verified boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    CONSTRAINT account_role_check CHECK (((role)::text = ANY ((ARRAY['patient'::character varying, 'doctor'::character varying, 'employee'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.account OWNER TO hmsdb_owner ;

--
-- Name: appointment; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.appointment (
    appointment_id character varying(100) NOT NULL,
    patient_id character varying(100) NOT NULL,
    doctor_id character varying(100) NOT NULL,
    request_date date NOT NULL,
    appointment_time time without time zone,
    status character varying(50),
    appointment_date date NOT NULL
);


ALTER TABLE public.appointment OWNER TO hmsdb_owner ;

--
-- Name: department; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.department (
    department_id character varying(100) NOT NULL,
    department_name character varying(100) NOT NULL
);


ALTER TABLE public.department OWNER TO hmsdb_owner ;

--
-- Name: disease; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.disease (
    disease_id uuid DEFAULT gen_random_uuid() NOT NULL,
    disease_name character varying(100) NOT NULL
);


ALTER TABLE public.disease OWNER TO hmsdb_owner ;

--
-- Name: doctor; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.doctor (
    doctor_id character varying(100) DEFAULT 'gen_doctor_id()'::character varying NOT NULL,
    full_name character varying(100) NOT NULL,
    birth_date date,
    gender character varying(10),
    address character varying(255),
    phone_number character varying(20) NOT NULL,
    national_id character varying(100),
    email character varying(100),
    experience integer,
    department_id character varying(100),
    CONSTRAINT doctor_experience_check CHECK ((experience >= 0)),
    CONSTRAINT doctor_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);


ALTER TABLE public.doctor OWNER TO hmsdb_owner ;

--
-- Name: doctor_seq; Type: SEQUENCE; Schema: public; Owner: hmsdb_owner 
--

CREATE SEQUENCE public.doctor_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.doctor_seq OWNER TO hmsdb_owner ;

--
-- Name: employee; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.employee (
    employee_id character varying(100) NOT NULL,
    full_name character varying(100) NOT NULL,
    birth_date date,
    gender character varying(10),
    address character varying(255),
    phone_number character varying(20) NOT NULL,
    national_id character varying(100),
    email character varying(100),
    "position" character varying(50) NOT NULL,
    department_id character varying(100),
    CONSTRAINT employee_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);


ALTER TABLE public.employee OWNER TO hmsdb_owner ;

--
-- Name: employee_seq; Type: SEQUENCE; Schema: public; Owner: hmsdb_owner 
--

CREATE SEQUENCE public.employee_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_seq OWNER TO hmsdb_owner ;

--
-- Name: insurance; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.insurance (
    insurance_id character varying(100) NOT NULL,
    patient_id character varying(100) NOT NULL,
    treatment_facility character varying(255)
);


ALTER TABLE public.insurance OWNER TO hmsdb_owner ;

--
-- Name: invoice; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.invoice (
    invoice_id character varying(100) NOT NULL,
    total_amount numeric(15,2),
    expense numeric(15,2),
    payment_date date,
    status character varying(50),
    employee_id character varying(100),
    CONSTRAINT invoice_expense_check CHECK ((expense >= (0)::numeric)),
    CONSTRAINT invoice_total_amount_check CHECK ((total_amount >= (0)::numeric))
);


ALTER TABLE public.invoice OWNER TO hmsdb_owner ;

--
-- Name: medical_examination; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.medical_examination (
    exam_id character varying(100) NOT NULL,
    patient_id character varying(100) NOT NULL,
    doctor_id character varying(100) NOT NULL,
    exam_date date NOT NULL,
    symptoms text,
    diagnosis text,
    treatment text,
    disease_id uuid
);


ALTER TABLE public.medical_examination OWNER TO hmsdb_owner ;

--
-- Name: medical_record; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.medical_record (
    record_id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id character varying(100) NOT NULL,
    doctor_id character varying(100) NOT NULL,
    exam_date date NOT NULL,
    symptoms text,
    diagnosis text,
    treatment text,
    department_id character varying(100)
);


ALTER TABLE public.medical_record OWNER TO hmsdb_owner ;

--
-- Name: medicine; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.medicine (
    medicine_id character varying(100) NOT NULL,
    medicine_name character varying(100) NOT NULL,
    category character varying(50),
    unit character varying(100),
    price numeric(10,2),
    expiration_date date,
    notes text,
    CONSTRAINT medicine_price_check CHECK ((price >= (0)::numeric))
);


ALTER TABLE public.medicine OWNER TO hmsdb_owner ;

--
-- Name: patient; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.patient (
    patient_id character varying(100) NOT NULL,
    full_name character varying(100) NOT NULL,
    birth_date date,
    gender character varying(10),
    address character varying(255),
    national_id character varying(100),
    phone_number character varying(20) NOT NULL,
    email character varying(100),
    medical_history text,
    CONSTRAINT patient_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);


ALTER TABLE public.patient OWNER TO hmsdb_owner ;

--
-- Name: patient_id_seq; Type: SEQUENCE; Schema: public; Owner: hmsdb_owner 
--

CREATE SEQUENCE public.patient_id_seq
    START WITH 10000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patient_id_seq OWNER TO hmsdb_owner ;

--
-- Name: patient_seq; Type: SEQUENCE; Schema: public; Owner: hmsdb_owner 
--

CREATE SEQUENCE public.patient_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patient_seq OWNER TO hmsdb_owner ;

--
-- Name: prescription; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.prescription (
    medicine_id character varying(100) NOT NULL,
    doctor_id character varying(100) NOT NULL,
    patient_id character varying(100) NOT NULL,
    invoice_id character varying(100),
    quantity integer,
    prescription_date date,
    notes text,
    CONSTRAINT prescription_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.prescription OWNER TO hmsdb_owner ;

--
-- Name: room; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.room (
    room_id character varying(100) NOT NULL,
    room_type character varying(50) NOT NULL,
    bed_id character varying(50) NOT NULL,
    status character varying(50),
    department_id character varying(100)
);


ALTER TABLE public.room OWNER TO hmsdb_owner ;

--
-- Name: service; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.service (
    service_id uuid DEFAULT gen_random_uuid() NOT NULL,
    service_name character varying(100) NOT NULL,
    unit_price numeric(10,2),
    unit character varying(100),
    CONSTRAINT service_unit_price_check CHECK ((unit_price >= (0)::numeric))
);


ALTER TABLE public.service OWNER TO hmsdb_owner ;

--
-- Name: service_detail; Type: TABLE; Schema: public; Owner: hmsdb_owner 
--

CREATE TABLE public.service_detail (
    service_id uuid NOT NULL,
    patient_id character varying(100) NOT NULL,
    quantity integer,
    usage_date date NOT NULL,
    CONSTRAINT service_detail_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.service_detail OWNER TO hmsdb_owner ;

--
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.account (account_id, password_hash, otp, role, user_id, phone_number, is_verified, created_at, updated_at) FROM stdin;
f905c79e-d958-4d61-9558-91246fe4d8f4	$2b$12$Hz6tQThmKYxF80UxqGQhT.dUaVd8sEB9Bn4U7HqlQvsxRD2jCKoai	\N	\N	PAT-20250404-10008	0882921022	\N	\N	\N
650c70ca-2a87-4819-a3fe-f754525131e2	$2b$12$Hz6tQThmKYxF80UxqGQhT.dUaVd8sEB9Bn4U7HqlQvsxRD2jCKoai	\N	doctor	CTCH3276	0882921021	\N	\N	\N
791fc800-78a3-499a-8241-1d4eaadab318	$2b$12$Hz6tQThmKYxF80UxqGQhT.dUaVd8sEB9Bn4U7HqlQvsxRD2jCKoai	\N	doctor	TM5230	0882921023	\N	\N	\N
942bce6f-a09e-4d64-9b93-b1257639a2c8	$2b$12$ybcUni2ioGlsqgXKLgy7BOexDD5vLocSGss5/tb8Ge2yBSwGh6xoq	\N	\N	\N	+84 798699203	t	2025-04-04 12:26:37.859801	2025-04-04 12:26:37.859801
\.


--
-- Data for Name: appointment; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.appointment (appointment_id, patient_id, doctor_id, request_date, appointment_time, status, appointment_date) FROM stdin;
\.


--
-- Data for Name: department; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.department (department_id, department_name) FROM stdin;
CTCH	Chấn thương chỉnh hình
NTK	Ngoại thần kinh
TM	Tim mạch
\.


--
-- Data for Name: disease; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.disease (disease_id, disease_name) FROM stdin;
\.


--
-- Data for Name: doctor; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.doctor (doctor_id, full_name, birth_date, gender, address, phone_number, national_id, email, experience, department_id) FROM stdin;
CTCH3276	Phat Nguyen	2022-01-12	Male	153 Le Hong Phong	0882921021	056100458221	hmsdb_owner 9712@gmail.com	4	CTCH
TM5230	Phat Nguyen	2025-04-04	Male	150 Le Hong Phone	0882921023	059202019022	\N	4	TM
\.


--
-- Data for Name: employee; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.employee (employee_id, full_name, birth_date, gender, address, phone_number, national_id, email, "position", department_id) FROM stdin;
\.


--
-- Data for Name: insurance; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.insurance (insurance_id, patient_id, treatment_facility) FROM stdin;
\.


--
-- Data for Name: invoice; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.invoice (invoice_id, total_amount, expense, payment_date, status, employee_id) FROM stdin;
\.


--
-- Data for Name: medical_examination; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.medical_examination (exam_id, patient_id, doctor_id, exam_date, symptoms, diagnosis, treatment, disease_id) FROM stdin;
\.


--
-- Data for Name: medical_record; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.medical_record (record_id, patient_id, doctor_id, exam_date, symptoms, diagnosis, treatment, department_id) FROM stdin;
\.


--
-- Data for Name: medicine; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.medicine (medicine_id, medicine_name, category, unit, price, expiration_date, notes) FROM stdin;
\.


--
-- Data for Name: patient; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.patient (patient_id, full_name, birth_date, gender, address, national_id, phone_number, email, medical_history) FROM stdin;
PAT-20250404-10008	Phat Nguyen	2022-01-12	Male	153 Le Hong Phong	056100458222	0882921022	hmsdb_owner 9713@gmail.com	None
\.


--
-- Data for Name: prescription; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.prescription (medicine_id, doctor_id, patient_id, invoice_id, quantity, prescription_date, notes) FROM stdin;
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.room (room_id, room_type, bed_id, status, department_id) FROM stdin;
\.


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.service (service_id, service_name, unit_price, unit) FROM stdin;
\.


--
-- Data for Name: service_detail; Type: TABLE DATA; Schema: public; Owner: hmsdb_owner 
--

COPY public.service_detail (service_id, patient_id, quantity, usage_date) FROM stdin;
\.


--
-- Name: doctor_seq; Type: SEQUENCE SET; Schema: public; Owner: hmsdb_owner 
--

SELECT pg_catalog.setval('public.doctor_seq', 1, false);


--
-- Name: employee_seq; Type: SEQUENCE SET; Schema: public; Owner: hmsdb_owner 
--

SELECT pg_catalog.setval('public.employee_seq', 1, false);


--
-- Name: patient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hmsdb_owner 
--

SELECT pg_catalog.setval('public.patient_id_seq', 10009, true);


--
-- Name: patient_seq; Type: SEQUENCE SET; Schema: public; Owner: hmsdb_owner 
--

SELECT pg_catalog.setval('public.patient_seq', 1, false);


--
-- Name: account account_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_phone_number_key UNIQUE (phone_number);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (account_id);


--
-- Name: appointment appointment_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);


--
-- Name: department department_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (department_id);


--
-- Name: disease disease_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_pkey PRIMARY KEY (disease_id);


--
-- Name: doctor doctor_email_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_email_key UNIQUE (email);


--
-- Name: doctor doctor_national_id_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_national_id_key UNIQUE (national_id);


--
-- Name: doctor doctor_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_phone_number_key UNIQUE (phone_number);


--
-- Name: doctor doctor_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_pkey PRIMARY KEY (doctor_id);


--
-- Name: employee employee_email_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_email_key UNIQUE (email);


--
-- Name: employee employee_national_id_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_national_id_key UNIQUE (national_id);


--
-- Name: employee employee_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_phone_number_key UNIQUE (phone_number);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employee_id);


--
-- Name: insurance insurance_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.insurance
    ADD CONSTRAINT insurance_pkey PRIMARY KEY (insurance_id);


--
-- Name: invoice invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (invoice_id);


--
-- Name: medical_examination medical_examination_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_pkey PRIMARY KEY (exam_id);


--
-- Name: medical_record medical_record_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_pkey PRIMARY KEY (record_id);


--
-- Name: medicine medicine_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medicine
    ADD CONSTRAINT medicine_pkey PRIMARY KEY (medicine_id);


--
-- Name: patient patient_email_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_email_key UNIQUE (email);


--
-- Name: patient patient_national_id_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_national_id_key UNIQUE (national_id);


--
-- Name: patient patient_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_phone_number_key UNIQUE (phone_number);


--
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);


--
-- Name: prescription prescription_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_pkey PRIMARY KEY (medicine_id, doctor_id, patient_id);


--
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (room_id);


--
-- Name: service_detail service_detail_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.service_detail
    ADD CONSTRAINT service_detail_pkey PRIMARY KEY (service_id, patient_id);


--
-- Name: service service_pkey; Type: CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.service
    ADD CONSTRAINT service_pkey PRIMARY KEY (service_id);


--
-- Name: ix_account_account_id; Type: INDEX; Schema: public; Owner: hmsdb_owner 
--

CREATE INDEX ix_account_account_id ON public.account USING btree (account_id);


--
-- Name: ix_disease_disease_id; Type: INDEX; Schema: public; Owner: hmsdb_owner 
--

CREATE INDEX ix_disease_disease_id ON public.disease USING btree (disease_id);


--
-- Name: ix_medical_record_record_id; Type: INDEX; Schema: public; Owner: hmsdb_owner 
--

CREATE INDEX ix_medical_record_record_id ON public.medical_record USING btree (record_id);


--
-- Name: ix_service_service_id; Type: INDEX; Schema: public; Owner: hmsdb_owner 
--

CREATE INDEX ix_service_service_id ON public.service USING btree (service_id);


--
-- Name: doctor after_insert_doctor; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER after_insert_doctor AFTER INSERT ON public.doctor FOR EACH ROW EXECUTE FUNCTION public.update_account_user_id();


--
-- Name: doctor after_insert_doctor1; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER after_insert_doctor1 AFTER INSERT ON public.doctor FOR EACH ROW EXECUTE FUNCTION public.update_account_role();


--
-- Name: employee after_insert_employee; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER after_insert_employee AFTER INSERT ON public.employee FOR EACH ROW EXECUTE FUNCTION public.update_account_user_id();


--
-- Name: employee after_insert_employee1; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER after_insert_employee1 AFTER INSERT ON public.employee FOR EACH ROW EXECUTE FUNCTION public.update_account_role();


--
-- Name: patient after_insert_patient; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER after_insert_patient AFTER INSERT ON public.patient FOR EACH ROW EXECUTE FUNCTION public.update_account_user_id();


--
-- Name: patient after_insert_patient1; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER after_insert_patient1 AFTER INSERT ON public.patient FOR EACH ROW EXECUTE FUNCTION public.update_account_role();


--
-- Name: department before_insert_department; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER before_insert_department BEFORE INSERT ON public.department FOR EACH ROW EXECUTE FUNCTION public.generate_dept_id();


--
-- Name: doctor before_insert_doctor; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER before_insert_doctor BEFORE INSERT ON public.doctor FOR EACH ROW EXECUTE FUNCTION public.generate_doctor_id();


--
-- Name: doctor before_insert_doctor1; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER before_insert_doctor1 BEFORE INSERT ON public.doctor FOR EACH ROW EXECUTE FUNCTION public.check_duplicate_data();


--
-- Name: employee before_insert_employee1; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER before_insert_employee1 BEFORE INSERT ON public.employee FOR EACH ROW EXECUTE FUNCTION public.check_duplicate_data();


--
-- Name: patient before_insert_patient; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER before_insert_patient BEFORE INSERT ON public.patient FOR EACH ROW EXECUTE FUNCTION public.generate_patient_id();


--
-- Name: patient before_insert_patient1; Type: TRIGGER; Schema: public; Owner: hmsdb_owner 
--

CREATE TRIGGER before_insert_patient1 BEFORE INSERT ON public.patient FOR EACH ROW EXECUTE FUNCTION public.check_duplicate_data();


--
-- Name: appointment appointment_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- Name: appointment appointment_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
-- Name: doctor doctor_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
-- Name: doctor doctor_phone_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_phone_number_fkey FOREIGN KEY (phone_number) REFERENCES public.account(phone_number);


--
-- Name: employee employee_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
-- Name: employee employee_phone_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_phone_number_fkey FOREIGN KEY (phone_number) REFERENCES public.account(phone_number);


--
-- Name: insurance insurance_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.insurance
    ADD CONSTRAINT insurance_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
-- Name: invoice invoice_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id);


--
-- Name: medical_examination medical_examination_disease_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_disease_id_fkey FOREIGN KEY (disease_id) REFERENCES public.disease(disease_id);


--
-- Name: medical_examination medical_examination_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- Name: medical_examination medical_examination_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
-- Name: medical_record medical_record_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
-- Name: medical_record medical_record_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- Name: medical_record medical_record_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
-- Name: patient patient_phone_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_phone_number_fkey FOREIGN KEY (phone_number) REFERENCES public.account(phone_number);


--
-- Name: prescription prescription_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- Name: prescription prescription_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoice(invoice_id);


--
-- Name: prescription prescription_medicine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicine(medicine_id);


--
-- Name: prescription prescription_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
-- Name: room room_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
-- Name: service_detail service_detail_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.service_detail
    ADD CONSTRAINT service_detail_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
-- Name: service_detail service_detail_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hmsdb_owner 
--

ALTER TABLE ONLY public.service_detail
    ADD CONSTRAINT service_detail_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.service(service_id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO hmsdb_owner ;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO hmsdb_owner ;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO hmsdb_owner ;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLES TO hmsdb_owner ;


--
-- PostgreSQL database dump complete
--

